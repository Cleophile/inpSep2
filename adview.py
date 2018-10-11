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
        self.initUI()

        # 还有timeinterval设定等等的信息

    def initUI(self):
        self.sas_label = QLabel("SAS位置：",self)
        self.sas_label.move(10,10)
        self.sas_label.resize(self.sas_label.sizeHint()*1.6)

        self.sas_input = QLineEdit(None,self)
        self.sas_input.resize(280,30)
        self.sas_input.move(10,40)
        self.sas_input.setText(self.info_list[0])

        self.total_time_label = QLabel("最大可接受运行时间",self)
        self.total_time_label.move(10,80)
        self.total_time_label.resize(self.total_time_label.sizeHint()*1.6)

        self.total_time_input = QLineEdit(None,self)
        self.total_time_input.move(10,110)
        self.total_time_input.resize(100,30)
        self.total_time_input.setText(str(self.info_list[1]))

        self.confirm_button = QPushButton("确定",self)
        self.confirm_button.move(140,110)
        self.confirm_button.resize(self.confirm_button.sizeHint())
        self.confirm_button.clicked.connect(self.confirm_pushed)

        self.cancel_button = QPushButton("取消",self)
        self.cancel_button.move(210,110)
        self.cancel_button.resize(self.cancel_button.sizeHint())
        self.cancel_button.clicked.connect(self.cancel_pushed)

        self.setGeometry(536,465,300,165)
        self.setWindowTitle("高级设置")
        # self.show()

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


