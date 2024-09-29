import os
import sys
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget, QLineEdit, QTextEdit, QComboBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
import S_DES
from S_DES import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("S-DES 加密系统")
        self.setGeometry(0, 0, 1000, 600)
        center(self)

        font = QFont("Arial", 12)
        self.setFont(font)

        main_layout = QVBoxLayout()

        button_layout = QHBoxLayout()

        self.home_button = QPushButton("首页")
        self.endecrypt_button = QPushButton("加解密")
        self.keygen_button = QPushButton("获取密钥")
        self.bruteforce_button = QPushButton("暴力破解")

        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 20px 40px;
                border-radius: 50px;
                font-size: 30px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        self.home_button.setStyleSheet(button_style)
        self.endecrypt_button.setStyleSheet(button_style)
        self.keygen_button.setStyleSheet(button_style)
        self.bruteforce_button.setStyleSheet(button_style)

        button_layout.addWidget(self.home_button)
        button_layout.addWidget(self.endecrypt_button)
        button_layout.addWidget(self.keygen_button)
        button_layout.addWidget(self.bruteforce_button)

        self.home_button.clicked.connect(self.show_home)
        self.endecrypt_button.clicked.connect(self.show_endecrypt)
        self.keygen_button.clicked.connect(self.show_keygen)
        self.bruteforce_button.clicked.connect(self.show_bruteforce)

        self.stacked_widget = QStackedWidget()

        self.home_page = self.create_home_page()
        self.endecrypt_page = self.create_endecrypt_page()
        self.keygen_page = self.create_keygen_page()
        self.bruteforce_page = self.create_bruteforce_page()

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.endecrypt_page)
        self.stacked_widget.addWidget(self.keygen_page)
        self.stacked_widget.addWidget(self.bruteforce_page)

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.stacked_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


    def show_home(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_endecrypt(self):
        self.stacked_widget.setCurrentWidget(self.endecrypt_page)

    def show_keygen(self):
        self.stacked_widget.setCurrentWidget(self.keygen_page)

    def show_bruteforce(self):
        self.stacked_widget.setCurrentWidget(self.bruteforce_page)

    # 创建首页
    def create_home_page(self):
        page = QWidget()
        self.setWindowIcon(QIcon(get_resource_path("img/app_icon.ico")))
        vbox = QVBoxLayout()
        label = QLabel("欢迎来到 DES 加密系统首页")
        label.setAlignment(Qt.AlignCenter)
        font = QFont("黑体", 30, QFont.Bold)
        label.setFont(font)
        label.setStyleSheet("color: #333;")

        vbox.addWidget(label)

        image_label = QLabel()
        pixmap = QPixmap(get_resource_path("img/logic.png"))
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        vbox.addWidget(image_label)

        vbox.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        copyright_label = QLabel('© 小胡不带小刘')
        copyright_label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(copyright_label)

        page.setLayout(vbox)

        return page

    # 创建加解密界面
    def create_endecrypt_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        font = QFont("Arial", 20)

        # 使用下拉框实现功能的变换
        self.combo_box1 = QComboBox()
        self.combo_box1.addItem("二进制加解密")
        self.combo_box1.addItem("ASCII 加解密")
        self.combo_box1.addItem("Unicode 加解密")
        self.combo_box1.setFont(font)
        self.combo_box1.setMinimumHeight(100)
        self.combo_box1.currentIndexChanged.connect(self.change_endecryption_type)

        # 初始设置位二进制加解密
        self.change_endecryption_type(0)
        layout.addWidget(self.combo_box1)

        self.hint_label = QLabel('提示：')
        self.hint_label.setWordWrap(True)
        self.hint_label.setFont(font)
        layout.addWidget(self.hint_label)

        plaintext_label = QLabel("明文")
        plaintext_label.setFont(font)
        self.plaincipher_input = QLineEdit()
        self.plaincipher_input.setPlaceholderText("请输入明文或密文")
        self.plaincipher_input.setFont(font)
        self.plaincipher_input.setMinimumHeight(100)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(plaintext_label)
        hbox1.addWidget(self.plaincipher_input)

        key_label = QLabel("密钥")
        key_label.setFont(font)
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("请输入密钥")
        self.key_input.setFont(font)
        self.key_input.setMinimumHeight(100)
        self.key_input.setEchoMode(QLineEdit.Password)  # 设置为密码模式，输入内容将被隐藏

        hbox2 = QHBoxLayout()
        hbox2.addWidget(key_label)
        hbox2.addWidget(self.key_input)

        result_label = QLabel("加密或解密结果")
        result_label.setFont(font)
        self.enderesult_display = QTextEdit()
        self.enderesult_display.setReadOnly(True)
        self.enderesult_display.setFont(font)
        self.enderesult_display.setMinimumHeight(100)

        encrypt_button = QPushButton("加密")
        decrypt_button = QPushButton("解密")
        encrypt_button.setFont(font)
        decrypt_button.setFont(font)
        encrypt_button.setMinimumHeight(50)
        decrypt_button.setMinimumHeight(50)
        encrypt_button.setMinimumWidth(100)
        decrypt_button.setMinimumWidth(100)

        encrypt_button.clicked.connect(self.encrypt)
        decrypt_button.clicked.connect(self.decrypt)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(encrypt_button)
        hbox3.addWidget(decrypt_button)

        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(result_label)
        layout.addWidget(self.enderesult_display)
        layout.addLayout(hbox3)

        back_button = QPushButton("返回")
        back_button.setFont(font)
        back_button.setMinimumHeight(50)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        copyright_label = QLabel('© 小胡不带小刘')
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setFont(QFont("Arial", 12))
        layout.addWidget(copyright_label)

        page.setLayout(layout)

        self.update_hints()

        return page

    # 创建生成密钥界面
    def create_keygen_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        font = QFont("Arial", 20)

        self.key_display = QLineEdit()
        self.key_display.setReadOnly(True)
        self.key_display.setPlaceholderText('生成的密钥会在这里显示')
        self.key_display.setFont(font)
        self.key_display.setMinimumHeight(100)
        self.key_display.setMaximumHeight(100)
        layout.addWidget(self.key_display)

        layout.addStretch()

        generate_button = QPushButton('生成密钥')
        generate_button.setFont(font)
        generate_button.setMinimumHeight(50)
        generate_button.clicked.connect(self.generate_key)

        back_button = QPushButton('返回')
        back_button.setFont(font)
        back_button.setMinimumHeight(50)
        back_button.clicked.connect(self.go_back)

        layout.addWidget(generate_button)
        layout.addWidget(back_button)

        copyright_label = QLabel('© 小胡不带小刘')
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setFont(QFont("Arial", 12))
        layout.addWidget(copyright_label)

        page.setLayout(layout)
        return page

    # 创建暴力破解界面
    def create_bruteforce_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        font = QFont("Arial", 20)

        # 也通过下拉框进行选择
        self.combo_box2 = QComboBox()
        self.combo_box2.addItem("二进制暴力破解")
        self.combo_box2.addItem("ASCII 暴力破解")
        self.combo_box2.addItem("Unicode 暴力破解")
        self.combo_box2.setFont(font)
        self.combo_box2.setMinimumHeight(100)
        layout.addWidget(self.combo_box2)

        self.tip_label = QLabel('提示：')
        self.tip_label.setWordWrap(True)
        self.tip_label.setFont(font)
        layout.addWidget(self.tip_label)

        plaintext_label = QLabel('明文')
        plaintext_label.setFont(font)
        self.plaintext_input = QLineEdit()
        self.plaintext_input.setPlaceholderText('请输入明文')
        self.plaintext_input.setFont(font)
        self.plaintext_input.setMinimumHeight(100)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(plaintext_label)
        hbox1.addWidget(self.plaintext_input)

        ciphertext_label = QLabel('密文')
        ciphertext_label.setFont(font)
        self.ciphertext_input = QLineEdit()
        self.ciphertext_input.setPlaceholderText('请输入密文')
        self.ciphertext_input.setFont(font)
        self.ciphertext_input.setMinimumHeight(100)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(ciphertext_label)
        hbox2.addWidget(self.ciphertext_input)

        result_label = QLabel('暴力破解结果')
        result_label.setFont(font)
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFont(font)
        self.result_display.setMinimumHeight(100)

        # 显示时间
        time_label = QLabel('破解耗时')
        time_label.setFont(font)
        self.time_display = QLabel('')

        force_button = QPushButton('暴力破解')
        back_button = QPushButton('返回')
        force_button.setFont(font)
        back_button.setFont(font)
        force_button.setMinimumHeight(50)
        back_button.setMinimumHeight(50)

        force_button.clicked.connect(self.force)
        back_button.clicked.connect(self.go_back)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(force_button)
        hbox3.addWidget(back_button)

        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(result_label)
        layout.addWidget(self.result_display)
        layout.addWidget(time_label)
        layout.addWidget(self.time_display)
        layout.addLayout(hbox3)

        copyright_label = QLabel('© 小胡不带小刘')
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setFont(QFont("Arial", 12))
        layout.addWidget(copyright_label)

        page.setLayout(layout)

        self.update_tips()

        return page

    def update_hints(self):
        hint_text = (
            "1. 二进制加解密要求明密文为8位的01组合。\n"
            "2. 密钥要求为10位的01组合。\n"
            "3. 请确保输入格式正确。"
        )
        self.hint_label.setText(hint_text)

    def update_tips(self):
        tip_text = (
            "1. 二进制暴力破解要求明密文为8位的01组合。\n"
            "2. ASCII和Unicode暴力破解要求明密文长度一致。\n"
            "3. 请确保输入格式正确。"
        )
        self.tip_label.setText(tip_text)

    # 通过index确定当前选择的模式，切换对应的在S_DES定义好的函数
    def change_endecryption_type(self, index):
        if index == 0:
            self.current_encrypt = S_DES.encrypt
            self.current_decrypt = S_DES.decrypt
        elif index == 1:
            self.current_encrypt = S_DES.encryptASC
            self.current_decrypt = S_DES.decryptASC
        elif index == 2:
            self.current_encrypt = S_DES.encryptUnicode
            self.current_decrypt = S_DES.decryptUnicode

    # 加密接口，连接S_DES里的函数和窗口里面输入字符的读取
    def encrypt(self):
        plaintext = self.plaincipher_input.text()
        key = self.key_input.text()

        if self.combo_box1.currentIndex() == 0:
            if not all(c in '01' for c in plaintext):
                self.enderesult_display.setText("错误：二进制明文输入只能包含 0 和 1。")
                return
            if len(plaintext) != 8:
                self.enderesult_display.setText("错误：输入的二进制明文必须为 8 位。")
                return
        elif self.combo_box1.currentIndex() == 1:
            if not all(0 <= ord(c) < 256 for c in plaintext):  # 校验输入的每个字符是否为有效 ASCII
                self.enderesult_display.setText("错误：请输入正确的 ASCII 字符。")
                return

        if not all(c in '01' for c in key):
            self.enderesult_display.setText("错误：密钥只能包含 0 和 1。")
            return
        if len(key) != 10:
            self.enderesult_display.setText("错误：密钥必须为 10 位。")
            return

        encrypted_text = self.current_encrypt(plaintext, key)
        self.enderesult_display.setText(encrypted_text)

    # 解密接口，连接S_DES里的函数和窗口里面输入字符的读取
    def decrypt(self):
        ciphertext = self.plaincipher_input.text()
        key = self.key_input.text()

        if self.combo_box1.currentIndex() == 0:
            if not all(c in '01' for c in ciphertext):
                self.enderesult_display.setText("错误：二进制密文输入只能包含 0 和 1。")
                return
            if len(ciphertext) != 8:
                self.enderesult_display.setText("错误：输入的二进制密文必须为 8 位。")
                return
        elif self.combo_box1.currentIndex() == 1:
            if not all(0 <= ord(c) < 256 for c in ciphertext):  # 校验输入的每个字符是否为有效 ASCII
                self.enderesult_display.setText("错误：请输入正确的 ASCII 字符。")
                return
        if not all(c in '01' for c in key):
            self.enderesult_display.setText("错误：密钥只能包含 0 和 1。")
            return
        if len(key) != 10:
            self.enderesult_display.setText("错误：密钥必须为 10 位。")
            return

        decrypted_text = self.current_decrypt(ciphertext, key)
        self.enderesult_display.setText(decrypted_text)

    # 生成密钥接口，连接S_DES里的函数
    def generate_key(self):
        key = S_DES.generate_key(10)
        self.key_display.setText(key)

    # 暴力破解接口，连接S_DES里的函数和窗口里面输入字符的读取
    def force(self):
        plaintext = self.plaintext_input.text()
        ciphertext = self.ciphertext_input.text()

        if self.combo_box2.currentIndex() == 0:
            if len(plaintext) != 8 or not all(c in '01' for c in plaintext):
                self.result_display.setPlainText('错误：明文必须是8位的01组合。')
                return
            if len(ciphertext) != 8 or not all(c in '01' for c in ciphertext):
                self.result_display.setPlainText('错误：密文必须是8位的01组合。')
                return

        elif self.combo_box2.currentIndex() in [1, 2]:
            if len(plaintext) != len(ciphertext):
                self.result_display.setPlainText('错误：明密文长度必须一致。')
                return

        # 通过currentIndex确定当前选择的模式，切换对应的在S_DES定义好的函数
        if self.combo_box2.currentIndex() == 0:
            results, elapsed_time = S_DES.force(plaintext, ciphertext)
        elif self.combo_box2.currentIndex() == 1:
            results, elapsed_time = S_DES.forceASC(plaintext, ciphertext)
        elif self.combo_box2.currentIndex() == 2:
            results, elapsed_time = S_DES.forceUnicode(plaintext, ciphertext)
        if results :
            self.result_display.setPlainText('\n'.join(results))
        else:
            self.result_display.setPlainText("未找到任何密钥")
        self.time_display.setText(f"耗时: {elapsed_time:.6f} 秒")

    # 返回，显示首页
    def go_back(self):
        self.show_home()


# 为了打包函数而用
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
