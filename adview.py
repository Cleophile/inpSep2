#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class advance_view(QWidget):
    def __init__(self,info_list=['./sas',600]):
        super().__init__()
        self.info_list = info_list
        self.plain_text_font = QFont()
        self.plain_text_font.setPointSize(13)
        self.initUI()
        self.setAcceptDrops(True)

    def initUI(self):
        self.vbox = QVBoxLayout() # MAIN box

        self.sas_label = QLabel("SAS位置：")
        # self.sas_label.move(10,10)
        self.sas_label.resize(104,30)
        self.sas_label.setFont(self.plain_text_font)

        self.vbox.addWidget(self.sas_label)

        self.line2 = QHBoxLayout()
        self.vbox.addLayout(self.line2)

        self.sas_input = QLineEdit(self.info_list[0])
        self.sas_input.resize(233,30)
        # self.sas_input.move(10,40)
        self.sas_input.setFont(self.plain_text_font)

        self.line2.addWidget(self.sas_input)
        
        self.browser_button = QPushButton("浏览")
        self.browser_button.resize(58,32)
        self.browser_button.setFont(self.plain_text_font)
        # self.browser_button.move(246,40)
        self.browser_button.clicked.connect(self.browser_action)

        self.line2.addWidget(self.browser_button)

        self.total_time_label = QLabel("最大可接受运行时间")
        # self.total_time_label.move(10,80)
        self.total_time_label.resize(187,30)
        self.total_time_label.setFont(self.plain_text_font)

        self.vbox.addWidget(self.total_time_label)

        self.line4 = QHBoxLayout()
        self.vbox.addLayout(self.line4)

        self.total_time_input = QLineEdit(str(self.info_list[1]))
        # self.total_time_input.move(10,110)
        self.total_time_input.resize(100,30)

        self.line4.addWidget(self.total_time_input)

        self.confirm_button = QPushButton("确定")
        # self.confirm_button.move(140,110)
        self.confirm_button.resize(68,32)
        self.confirm_button.clicked.connect(self.confirm_pushed)
        self.confirm_button.setFont(self.plain_text_font)

        self.line4.addWidget(self.confirm_button)

        self.cancel_button = QPushButton("取消")
        # self.cancel_button.move(210,110)
        self.cancel_button.resize(68,32)
        self.cancel_button.clicked.connect(self.cancel_pushed)
        self.cancel_button.setFont(self.plain_text_font)

        self.line4.addWidget(self.cancel_button)

        self.setGeometry(536,465,300,165)
        self.setWindowTitle("高级设置")
        self.setLayout(self.vbox)
        # self.show()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls(): # 设定好接受拖拽的数据类型（plain text）
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e): # 更改按钮接受鼠标的释放事件的默认行为
        # self.file_position_input_box.text = str(e.mimeData().urls())
        urlList = []
        for url in e.mimeData().urls():
            urlList.append(str(url.toLocalFile()))
        if len(urlList) == 1:
            self.sas_input.setText(urlList[0])
        else:
            QMessageBox.warning(self, '警告', '拖放文件时的未知错误', QMessageBox.Ok)

    def browser_action(self):
        browsed_path = QFileDialog.getOpenFileUrl(self, "Browser", ".")
        this_path = browsed_path[0].toLocalFile()
        this_path.replace(r'file://','')
        self.sas_input.setText(this_path)

    def confirm_pushed(self):
        try :
            self.info_list[0] = self.sas_input.text()
            self.info_list[1] = float(self.total_time_input.text())
            self.close()
        except :
            QMessageBox.warning(self,"警告","设置失败",QMessageBox.Ok)

    def cancel_pushed(self):
        self.close()
    
    def handle_click(self):
        if not self.isVisible():
            self.show()


if __name__ == "__main__":
    app=QApplication(sys.argv)
    w = advance_view()
    w.show()
    sys.exit(app.exec_())


