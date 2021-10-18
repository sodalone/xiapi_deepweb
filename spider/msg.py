from PyQt5.QtWidgets import *


def messageDialog():
    # 核心功能代码就两行，可以加到需要的地方
    msg_box = QMessageBox(QMessageBox.Warning, '提示', '下载成功')
    msg_box.exec_()
