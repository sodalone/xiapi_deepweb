import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog
from functools import partial
import pandas as pd
import csv

import search_keyword
import search_similar

from time import sleep


import sousuo  # 主页
import child1  # 是否继续对话框
import child2  # 导出对话框
import msg  # 提示框

'''
初始化主界面
'''


def clearMain(ui, message):
    ui.lineEdit1.setText("")
    message = []

'''
根据搜索提示框打开结果框，结果框中提示本次爬虫结果并让用户选择是否继续
'''


def convert(ui1, ui2, message, target):  # ui1为主界面 ui2为子界面对话框
    input = ui1.lineEdit1.text()
    target = input
    demo = search_keyword.SearchKeyword(key_word=input, thread_count=1)
    demo.start()
    sleep(10)
    '''
    此处进行根据input内容进行爬虫，并生成提示
    '''
    # message中第一个元素变为提示结果
    messageFirst="第1次爬虫结果共爬到"+str(len(demo.find_goods))+"个数据，点击继续将根据这些结果，选取其相似商品进行爬取，点击导出可导出结果"
    message.append(messageFirst)
    # 将爬虫的提示结果填充至继续对话框的textEdit1框中
    ui2.textEdit1.setText(str(message[-1]))


'''
在导出对话框中如果选择"导出"将弹出导出的对话框，在此处选择路径
此功能提示用户选择路径并将路径展示到屏幕上
'''


def openFile(ui):
    get_directory_path = QFileDialog.getExistingDirectory()
    ui.outDir.setText(str(get_directory_path))


'''
在导出对话框根据所输出路径进行下载并弹出下载成功与否的对话框
'''


def downloadFromDir(ui):
    get_directory_path = ui.outDir.text();
    # 下载功能
    msg.messageDialog()


'''
重新进行爬虫，并更新提示信息
'''


def setAgain(message, target):
    print(target)
    iterator_count = len(message)
    key_word = "炮"
    demo = search_similar.SearchSimilar(key_word=key_word, iterator_count=iterator_count, thread_count=10)
    demo.start()
    sleep(100)
    print("等待结束")
    demo.csv_writer.writerows(demo.write_datas)
    df = pd.read_csv(demo.now_file, encoding='utf-8_sig', keep_default_na=False)
    df = df.drop_duplicates()
    data_increase = len(df) - len(demo.is_similar)
    df.to_csv(demo.now_file, index=False, encoding='utf-8_sig')

    message.append("第"+str(len(message)+1)+"次爬虫结果共爬到"+"一共新增"+str(data_increase))  # 原为字符串后续更新该字符串


'''
将更新后的爬虫信息重新填入是否继续的对话框
'''


def getAgain(ui, message):
    ui.textEdit1.setText(str(message[-1]))


'''
以下是mian函数
'''
if __name__ == '__main__':
    message = [];
    target = ""
    app = QApplication(sys.argv)
    # 实例化主窗口
    MainWindow = QMainWindow()
    mian_ui = sousuo.Ui_MainWindow()
    mian_ui.setupUi(MainWindow)

    # 实例化子窗口1
    ChildWindow1 = QDialog()
    child_ui1 = child1.Ui_Dialog()
    child_ui1.setupUi(ChildWindow1)

    # 实例化子窗口2
    ChildWindow2 = QDialog()
    child_ui2 = child2.Ui_Dialog()
    child_ui2.setupUi(ChildWindow2)

    # 在主界面输入信息，并处理结果，将第一次结果传入是否继续的对话框
    mian_ui.pushButton1.clicked.connect(partial(convert, mian_ui, child_ui1, message, target))

    # 点击查询按钮，展示是否继续查询的对话框
    mian_ui.pushButton1.clicked.connect(ChildWindow1.show)

    # 在是否继续查询的对话框点击导出，弹出导出信息的对话框
    child_ui1.Push_back.clicked.connect(ChildWindow2.show)

    # 在是否继续查询的对话框点击继续爬虫，以下四个步骤展示新结果
    child_ui1.Push_Go.clicked.connect(partial(setAgain, message, target))  # 进行重新爬虫
    child_ui1.Push_Go.clicked.connect(ChildWindow1.close)  # 关闭当前的对话框
    child_ui1.Push_Go.clicked.connect(partial(getAgain, child_ui1, message))  # 再次填充是否继续查询的对话框
    child_ui1.Push_Go.clicked.connect(ChildWindow1.show)  # 显示更新后的对话框

    # 在导出对话框中点击选择路径，并将路径显示至文本框
    child_ui2.getDir.clicked.connect(partial(openFile, child_ui2))

    # 点击下载进行下载，下载成功后关闭出主对话框外的所有对话框,最后将主对话框中内容清空
    child_ui2.download.clicked.connect(partial(downloadFromDir, child_ui2))
    child_ui2.download.clicked.connect(ChildWindow2.close)
    child_ui2.download.clicked.connect(ChildWindow1.close)
    child_ui2.download.clicked.connect(partial(clearMain, mian_ui, message))

    MainWindow.show()
    sys.exit(app.exec_())
