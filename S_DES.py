import secrets
import time
from PyQt5.QtWidgets import QDesktopWidget


# 子密钥的生成
def subKey(input):
    p_10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    p_8 = [6, 3, 7, 4, 8, 5, 10, 9]
    leftShift_1 = [2, 3, 4, 5, 1]
    leftShift_2 = [3, 4, 5, 1, 2]
    temp = []
    # 按p10轮转对密钥进行处理
    for i in range(10):
        temp.append(int(input[p_10[i] - 1]))
    k1 = []
    k2 = []
    temp01 = []
    temp02 = []
    temp03 = []
    temp04 = []
    # 获得k1
    # 对密钥的左半边进行leftShift_1
    for i in range(5):
        temp01.append(temp[leftShift_1[i] - 1])
    # 对密钥的右半边进行leftShift_1
    for i in range(5):
        temp02.append(temp[leftShift_1[i] + 4])
    # 合并得到子密钥k1
    for i in range(8):
        k1.append((temp01 + temp02)[p_8[i] - 1])
    # 同理获得k2
    for i in range(5):
        temp03.append(temp[leftShift_2[i] - 1])
    for i in range(5):
        temp04.append(temp[leftShift_2[i] + 4])
    for i in range(8):
        k2.append((temp03 + temp04)[p_8[i] - 1])
    return [k1, k2]


# 初始置换函数
def permute(input):
    p_box = [2, 6, 3, 1, 4, 8, 5, 7]
    p_result = []
    for index in range(8):
        p_result.append(int(input[p_box[index] - 1]))
    return p_result


# 最终置换函数
def finalPermute(input):
    p_box = [4, 1, 3, 5, 7, 2, 8, 6]
    p_reverse_result = []
    for index in range(8):
        p_reverse_result.append(int(input[p_box[index] - 1]))
    return p_reverse_result


# 二进制转换(S-BOX)
def binary(a):
    if a == 3:
        return [1, 1]
    elif a == 2:
        return [1, 0]
    elif a == 1:
        return [0, 1]
    else:
        return [0, 0]


# 轮函数，输入的值分别为处理后的明文和子密钥
def round_function(Text, k):
    right = []
    left = []
    for index in range(4):
        left.append(int(Text[index]))
    for index in range(4):
        right.append(int(Text[index + 4]))
    EPBox = [4, 1, 2, 3, 2, 3, 4, 1]
    SBox_1 = [(1, 0, 3, 2), (3, 2, 1, 0), (0, 2, 1, 3), (3, 1, 0, 2)]
    SBox_2 = [(0, 1, 2, 3), (2, 3, 1, 0), (3, 0, 1, 2), (2, 1, 0, 3)]
    SPBox = [2, 4, 3, 1]
    expend_right = []
    # 对R半边进行拓展
    for index in range(8):
        expend_right.append(int(right[EPBox[index] - 1]))
    # 进行异或
    for index in range(8):
        if int(k[index]) == expend_right[index]:
            expend_right[index] = 0
        else:
            expend_right[index] = 1
    # 找到在矩阵中对应位置
    flag01 = expend_right[0] * 2 + expend_right[3] * 1
    flag02 = expend_right[1] * 2 + expend_right[2] * 1
    flag03 = expend_right[4] * 2 + expend_right[7] * 1
    flag04 = expend_right[5] * 2 + expend_right[6] * 1
    expend_right01 = SBox_1[flag01][flag02]
    expend_right02 = SBox_2[flag03][flag04]
    ans = binary(expend_right01) + binary(expend_right02)
    key_left = []
    # 轮转
    for index in range(4):
        key_left.append(ans[SPBox[index] - 1])
    # 异或
    for index in range(4):
        if key_left[index] == left[index]:
            key_left[index] = 0
        else:
            key_left[index] = 1
    return key_left + right


# 左右互换SW，输入一段8-bit的密文，函数会将其左右4-bit的内容调换
def swapper(input):
    right = []
    left = []
    for index in range(4):
        right.append(input[index])
    for index in range(4):
        left.append(input[index + 4])
    return left + right


# 加密函数
def encrypt(plainText,key):
    k1 = subKey(key)[0]
    k2 = subKey(key)[1]
    ip = permute(plainText)
    fk1 = round_function(ip, k1)
    sw = swapper(fk1)
    fk2 = round_function(sw, k2)
    ip_reverse = finalPermute(fk2)
    ip_str = ''.join(str(i) for i in ip_reverse)
    return ip_str


# 解密函数
def decrypt(cipherText,key):
    k1 = subKey(key)[0]
    k2 = subKey(key)[1]
    ip = permute(cipherText)
    fk2 = round_function(ip, k2)
    sw = swapper(fk2)
    fk1 = round_function(sw, k1)
    ip_reverse = finalPermute(fk1)
    ip_str = ''.join(str(i) for i in ip_reverse)
    return ip_str


# 加密ASCII函数
def encryptASC(plainText,key):
    encrypted_text = ''
    for char in plainText:
        binary_text = format(ord(char), '08b')
        k1 = subKey(key)[0]
        k2 = subKey(key)[1]
        ip = permute(binary_text)
        fk1 = round_function(ip, k1)
        sw = swapper(fk1)
        fk2 = round_function(sw, k2)
        ip_reverse = finalPermute(fk2)
        ip_str = ''.join(str(i) for i in ip_reverse)
        encrypted_text += chr(int(ip_str, 2))
    return encrypted_text


# 解密ASCII函数
def decryptASC(cipherText,key):
    decrypted_text = ''
    for char in cipherText:
        binary_text = format(ord(char), '08b')
        k1 = subKey(key)[0]
        k2 = subKey(key)[1]
        ip = permute(binary_text)
        fk2 = round_function(ip, k2)
        sw = swapper(fk2)
        fk1 = round_function(sw, k1)
        ip_reverse = finalPermute(fk1)
        ip_str = ''.join(str(i) for i in ip_reverse)
        decrypted_text += chr(int(ip_str, 2))
    return decrypted_text


# unicode转换为二进制
def unicode2binary(unicode_str):
    binary_list = []
    for char in unicode_str:
        unicode_val = ord(char)  # 获取字符的 Unicode 值
        binary_str = format(unicode_val, '016b')  # 转换为 16 位二进制字符串
        binary_list.append(binary_str)  # 存储二进制字符串
    return binary_list


# 加密unicode函数
def encryptUnicode(unicode_str, key):
    binary_list = unicode2binary(unicode_str)
    encrypted_unicode = ''

    for binary in binary_list:
        left = binary[:8]  # 高8位
        right = binary[8:]  # 低8位

        # 加密高8位和低8位
        encrypted_left = encrypt(left, key)
        encrypted_right = encrypt(right, key)

        # 合并加密后的结果
        combined_binary = encrypted_left + encrypted_right

        # 转换为Unicode字符并追加到结果
        unicode_char = chr(int(combined_binary, 2))  # 将二进制转换为整数，再转换为字符
        encrypted_unicode += unicode_char

    return encrypted_unicode


# 解密unicode函数
def decryptUnicode(unicode_str, key):
    binary_list = unicode2binary(unicode_str)
    decrypted_unicode = ''

    for binary in binary_list:
        left = binary[:8]  # 高8位
        right = binary[8:]  # 低8位

        # 加密高8位和低8位
        decrypted_left = decrypt(left, key)
        decrypted_right = decrypt(right, key)

        # 合并加密后的结果
        combined_binary = decrypted_left + decrypted_right

        # 转换为Unicode字符并追加到结果
        unicode_char = chr(int(combined_binary, 2))  # 将二进制转换为整数，再转换为字符
        decrypted_unicode += unicode_char

    return decrypted_unicode


# 暴力破解二进制
def force(plainText, cipherText):
    # 记录开始时间
    start_time = time.time()
    possible_keys = []
    # 遍历所有10位二进制密钥
    for key_int in range(1024):
        # 生成10位二进制密钥
        key = format(key_int, '010b')

        # 使用当前密钥对明文加密
        encrypted_text = encrypt(plainText, key)

        # 判断是否与给定的密文匹配
        if encrypted_text == cipherText:
            possible_keys.append(key)
    # 记录结束时间
    end_time = time.time()
    # 计算并打印程序运行时间
    elapsed_time = end_time - start_time
    # 打印破解结果
    if possible_keys:
        print(f"已找到密钥: {possible_keys}")
    else:
        print("未找到任何密钥")

    print(f"暴力破解完成, 耗时: {elapsed_time:.6f} 秒")

    return possible_keys,elapsed_time


# 暴力破解ASCII
def forceASC(plainText, cipherText):
    # 记录开始时间
    start_time = time.time()
    possible_keys = []
    # 遍历所有10位二进制密钥
    for key_int in range(1024):
        # 生成10位二进制密钥
        key = format(key_int, '010b')

        # 使用当前密钥对明文加密
        encrypted_text = encryptASC(plainText, key)

        # 判断是否与给定的密文匹配
        if encrypted_text == cipherText:
            possible_keys.append(key)
    # 记录结束时间
    end_time = time.time()
    # 计算并打印程序运行时间
    elapsed_time = end_time - start_time
    # 打印破解结果
    if possible_keys:
        print(f"已找到密钥: {possible_keys}")
    else:
        print("未找到任何密钥")

    print(f"暴力破解完成, 耗时: {elapsed_time:.6f} 秒")

    return possible_keys,elapsed_time


# 暴力破解unicode
def forceUnicode(plainText, cipherText):
    # 记录开始时间
    start_time = time.time()
    possible_keys = []
    # 遍历所有10位二进制密钥
    for key_int in range(1024):
        # 生成10位二进制密钥
        key = format(key_int, '010b')

        # 使用当前密钥对明文加密
        encrypted_text = encryptUnicode(plainText, key)

        # 判断是否与给定的密文匹配
        if encrypted_text == cipherText:
            possible_keys.append(key)
    # 记录结束时间
    end_time = time.time()
    # 计算并打印程序运行时间
    elapsed_time = end_time - start_time
    # 打印破解结果
    if possible_keys:
        print(f"已找到密钥: {possible_keys}")
    else:
        print("未找到任何密钥")

    print(f"暴力破解完成, 耗时: {elapsed_time:.6f} 秒")

    return possible_keys,elapsed_time


# 获取密钥函数
def generate_key(length):
    key = secrets.randbits(length)
    # 转为二进制，左零补全为10-bit
    key_bin = bin(key).replace('0b', '').zfill(10)
    return key_bin


# 居中页面函数
def center(self):
    # 获取屏幕的分辨率
    screen = QDesktopWidget().screenGeometry()
    # 获取窗口的尺寸
    size = self.geometry()
    # 计算出窗口左上角的点，使其居中
    x = (screen.width() - size.width()) // 2
    y = (screen.height() - size.height()) // 2
    self.move(x, y)
