#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

import analyzedataset
import alterdata
from adview import advance_view
import multiprocessing

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
import os
from copy import copy,deepcopy
import time
import psutil

THIS_SYSTEM = 'OTHERS'

if 'win32' in sys.platform:
    THIS_SYSTEM = 'WINDOWS'
if 'darwin' in sys.platform:
    THIS_SYSTEM = 'MACOS'

def index_by_times(iterable,obj,times):
    find_times = 0
    for count,l in enumerate(iterable):
        if l == obj:
            find_times += 1
        if find_times == times:
            return count
    else :
        return -1

# 线程定义
class WorkingThread(multiprocessing.Process):
    def __init__(self, function_name, inputName, outputName):  # , pid_list=pid_list
        super().__init__()
        self.name = 'WorkingThread'
        self.inputName = inputName
        self.outputName = outputName
        self.function_name = function_name
        # self.pid_list = pid_list

    def run(self):
        print('传输线程已经开始')
        cmd_line = '{} < {} > {}'.format(self.function_name, self.inputName, self.outputName)
        os.system(cmd_line)

class Window(QWidget):
    def __init__(self,sysargs):
        super().__init__()
        self.selected_points = []
        self.selected_randoms = []
        self.random_type_list = []
        self.random_number_type = {
                'normal': 0 ,# 高斯分布
                'uniform': 1,# 均匀分布
                'expotential': 2, # 指数分布
                'quadratic': 3 # 二次函数
                # 可以添加
                }
        self.logfile = sysargs[-1]
        self.didGenerateFiles = False
        self.current_folder_file_count = -1
        self.current_folder = None
        self.interval = 1
        self.info_list = ['./sas',600]
        if THIS_SYSTEM == 'WINDOWS':
            self.info_list[0] = r'.\sas.exe'
        self.initUI()
        self.setAcceptDrops(True)
    
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
            self.file_position_input_box.setText(urlList[0])
            self.show_data()
            self.writelog(5,'File path inserted by drag&patch')
        else:
            self.writelog(1,'Error when parsing file.')
            QMessageBox.warning(self, '警告', '拖放文件时的未知错误', QMessageBox.Ok)


    def writelog(self, msg_type, msg):
        type_dict = {
            1:'ERROR',
            2:'WARNING',
            3:'SEARCH',
            4:'GENERATE',
            5:'SYSTEM',
            6:'INPUT',
            7:'DEL',
            8:'TRANSMIT'
        }
        s = '[{}]@[{}] {}\n'.format(type_dict[msg_type],
                                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                                  ,msg)
        self.logfile.write(s)

    def clear_previous(self):
        self.fort_list = [i for i in os.listdir('.') if 'fort' in i]
        for fortname in self.fort_list:
            if THIS_SYSTEM == 'MACOS':
                os.system('rm ./{}'.format(fortname))
            if THIS_SYSTEM == 'WINDOWS':
                os.system(r'del .\{}'.format(fortname))

        if os.path.exists('./SAS.log'):
            if THIS_SYSTEM == 'MACOS':
                os.system('rm ./SAS.log')
            if THIS_SYSTEM == 'WINDOWS':
                os.system(r'del .\SAS.log')
        if os.path.exists('./SAS.pid'):
            if THIS_SYSTEM == 'MACOS':
                os.system('rm ./SAS.pid')
            if THIS_SYSTEM == 'WINDOWS':
                os.system(r'del .\SAS.pid')

        if os.path.exists('CHANNEL.dat'):
            if THIS_SYSTEM == 'MACOS':
                os.system('rm ./CHANNEL.dat')
            if THIS_SYSTEM == 'WINDOWS':
                os.system(r'del .\CHANNEL.dat')
        if os.path.exists('./INPUT.dat'):
            if THIS_SYSTEM == 'MACOS':
                os.system('rm ./INPUT.dat')
            if THIS_SYSTEM == 'WINDOWS':
                os.system(r'del .\INPUT.dat')

        if os.path.exists('./PRIMAR4.dat'):
            if THIS_SYSTEM == 'MACOS':
                os.system('rm ./PRIMAR4.dat')
            if THIS_SYSTEM == 'WINDOWS':
                os.system('del .\PRIMAR4.dat')

        if os.path.exists('./RESTART.dat'):
            if THIS_SYSTEM == 'MACOS':
                os.system('rm ./RESTART.dat')
            if THIS_SYSTEM == 'WINDOWS':
                os.system('del .\RESTART.dat')

        # One more deleting
    
    def initUI(self):
        self.plain_font_size = QFont()
        self.plain_font_size.setPointSize(12)
        self.writelog(5,'Initiating System UI Layout...')
        QToolTip.setFont(QFont('SansSerif', 10))
        # 需要添加一些输入模块
        line0=28
        line_start_pos = 55
        
        self.vbox = QVBoxLayout() # MAIN BOX
        self.line1 = QHBoxLayout()
        self.vbox.addLayout(self.line1)
        
        self.line1_empty = QLabel('')
        self.line1.addWidget(self.line1_empty,3)

        self.random_explain_label = QLabel("Gaussian Distribution", self)
        self.random_explain_label.resize(300,23)
        # self.random_explain_label.move(line_start_pos + 300, 5)
        self.random_explain_label.setFont(self.plain_font_size)
        # ===================================
        self.line1.addWidget(self.random_explain_label,1)

        self.line2 = QHBoxLayout()
        self.vbox.addLayout(self.line2)
        self.line2_left = QHBoxLayout()
        self.line2_right = QHBoxLayout()
        self.line2.addLayout(self.line2_left,3)
        self.line2.addLayout(self.line2_right,2)
        self.line2.setStretchFactor(self.line2_left, 2)
        self.line2.setStretchFactor(self.line2_right,1)

        self.number_of_randoms_label = QLabel("请输入随机数个数",self)
        self.number_of_randoms_label.resize(QSize(166, 30))
        # number_of_randoms_label.move(line_start_pos, line0)
        self.number_of_randoms_label.setFont(self.plain_font_size)
        self.line2_left.addWidget(self.number_of_randoms_label)

        self.number_of_randoms_input = QLineEdit(None, self)
        self.number_of_randoms_input.resize(35,30)
        # self.number_of_randoms_input.move(line_start_pos+111,line0)
        self.number_of_randoms_input.setFont(self.plain_font_size)
        self.line2_left.addWidget(self.number_of_randoms_input)
        # ====================================
        
        self.random_function_label = QLabel("请选择随机数生成方式:", self)
        self.random_function_label.resize(QSize(214, 30))
        # random_function_label.move(line_start_pos+161,line0)
        self.random_function_label.setFont(self.plain_font_size)
        self.line2_left.addWidget(self.random_function_label)
        
                
        # self.random_function_select = QRadioButton("选中为高斯分布, 否则为均匀分布", self)
        # self.random_function_select.resize(self.random_function_select.sizeHint()*1.6)
        # self.random_function_select.move(line_start_pos+300,line0-5)
        self.random_function_choose_list = QComboBox(self)
        # self.random_function_choose_list.move(line_start_pos+300, line0)
        for i in self.random_number_type.keys():
            self.random_function_choose_list.addItem(i)
        self.random_function_choose_list.currentIndexChanged.connect(self.show_complement_info)
        self.random_function_choose_list.resize(QSize(120, 30))
        self.random_function_choose_list.setFont(self.plain_font_size)
        self.line2_left.addWidget(self.random_function_choose_list)

        # complement section
        self.empty_line2 = QLabel('')
        self.line2_right.addWidget(self.empty_line2)

        self.complement_label_a = QLabel("a:", self)
        self.complement_label_a.resize(QSize(19, 26))
        # self.complement_label_a.move(line_start_pos + 432,line0)
        self.complement_label_a.setFont(self.plain_font_size)
        self.complement_label_a.hide()
        self.line2_right.addWidget(self.complement_label_a)

        self.complement_label_gamma = QLabel("γ:",self)
        self.complement_label_gamma.resize(QSize(19, 26))
        # self.complement_label_gamma.move(line_start_pos + 432,line0)
        self.complement_label_gamma.setFont(self.plain_font_size)
        self.complement_label_gamma.hide()
        self.line2_right.addWidget(self.complement_label_gamma)

        self.complement_first_insert = QLineEdit(None, self)
        self.complement_first_insert.resize(50,30)
        # self.complement_first_insert.move(line_start_pos + 450, line0)
        self.complement_first_insert.setFont(self.plain_font_size)
        self.complement_first_insert.hide()
        self.line2_right.addWidget(self.complement_first_insert)

        self.complement_label_b = QLabel("b:", self)
        self.complement_label_b.resize(QSize(19, 26))
        # self.complement_label_b.move(line_start_pos + 512, line0)
        self.complement_label_b.setFont(self.plain_font_size)
        self.complement_label_b.hide()
        self.line2_right.addWidget(self.complement_label_b)

        self.complement_second_insert = QLineEdit(None, self)
        self.complement_second_insert.resize(50, 30)
        # self.complement_second_insert.move(line_start_pos + 530, line0)
        self.complement_second_insert.setFont(self.plain_font_size)
        self.complement_second_insert.hide()
        self.line2_right.addWidget(self.complement_second_insert)

        self.complement_label_c = QLabel("c:", self)
        self.complement_label_c.resize(QSize(19, 26))
        # self.complement_label_c.move(line_start_pos + 592, line0)
        self.complement_label_c.setFont(self.plain_font_size)
        self.complement_label_c.hide()
        self.line2_right.addWidget(self.complement_label_c)

        self.complement_third_insert = QLineEdit(None, self)
        self.complement_third_insert.resize(50, 30)
        # self.complement_third_insert.move(line_start_pos + 610, line0)
        self.complement_third_insert.setFont(self.plain_font_size)
        self.complement_third_insert.hide()
        # end of complement section
        self.line2_right.addWidget(self.complement_third_insert)

        # 基本常数设定
        linegap=37
        line1 = linegap+line0
        # ====================================

        self.line3 = QHBoxLayout()
        self.vbox.addLayout(self.line3)

        # 输入文本位置的文本框提示符
        self.file_position_label = QLabel("请输入原始文件的位置",self)
        self.file_position_label.resize(QSize(208, 30))
        # file_position_label.move(line_start_pos, line1)
        self.file_position_label.setFont(self.plain_font_size)
        self.line3.addWidget(self.file_position_label)
        # ================================================

        # 用于输入文件位置的文本框 
        self.file_position_input_box = QLineEdit(None, self)
        # self.file_position_input_box.move(195, line1)
        self.file_position_input_box.resize(498,30)
        self.file_position_input_box.setFont(self.plain_font_size)
        self.line3.addWidget(self.file_position_input_box)
        # ================================================

        self.file_browser_button = QPushButton("浏览",self)
        self.file_browser_button.setFont(self.plain_font_size)
        # self.file_browser_button.move(697, line1)
        self.file_browser_button.resize(QSize(68,32))
        self.file_browser_button.clicked.connect(self.file_browser_action)
        self.line3.addWidget(self.file_browser_button)

        line2 = line1 + linegap
        self.line4 = QHBoxLayout()
        self.vbox.addLayout(self.line4)

        self.line4_left = QHBoxLayout()
        self.line4.addLayout(self.line4_left,3)
        self.empty_line4 = QLabel('')
        self.line4.addWidget(self.empty_line4,1)
        

        # 选定Block的提示框
        self.block_name_label = QLabel("请输入Block的名称", self)
        self.block_name_label.resize(QSize(179, 30))
        # block_name_label.move(line_start_pos, line2)
        self.block_name_label.setFont(self.plain_font_size)
        self.line4_left.addWidget(self.block_name_label)

        # 输入block的文本框
        self.block_name_input = QLineEdit(None,self)
        self.block_name_input.resize(220,30)
        # self.block_name_input.move(195,line2)
        self.block_name_input.setFont(self.plain_font_size)
        self.line4_left.addWidget(self.block_name_input)

        # 显示数据的按钮
        self.show_block_data_button = QPushButton("显示数据",self)
        self.show_block_data_button.resize(QSize(94, 35))
        # show_block_data_button.move(195+220+60, line2)
        self.show_block_data_button.clicked.connect(self.show_data)
        self.show_block_data_button.setFont(self.plain_font_size)
        self.line4_left.addWidget(self.show_block_data_button)

        # 更高级的方法：直接拖动 
        self.line5 = QHBoxLayout()
        self.vbox.addLayout(self.line5)
        self.line5_left = QHBoxLayout()
        self.line5_right = QHBoxLayout()
        self.line5.addLayout(self.line5_left,9)
        self.line5.addLayout(self.line5_right,2)
        self.empty_line5 = QLabel('')
        self.line5.addWidget(self.empty_line5,2)

        self.block_insert_label = QLabel("输入block的序数：", self)
        self.block_insert_label.resize(QSize(179, 30))
        # block_insert_label.move(line_start_pos, line3)
        self.block_insert_label.setFont(self.plain_font_size)
        self.line5_left.addWidget(self.block_insert_label)

        self.block_insert = QLineEdit(None,self)
        self.block_insert.resize(55, 30)
        # self.block_insert.move(line_start_pos+45+71, line3)
        self.block_insert.setFont(self.plain_font_size)
        self.line5_left.addWidget(self.block_insert)
        
        # 输入行位置的标签
        self.point_left_label = QLabel("请输入需要取的点  行：",self)
        self.point_left_label.resize(QSize(221, 30))
        # point_left_label.move(55+115+71, line3)
        self.point_left_label.setFont(self.plain_font_size)
        self.line5_left.addWidget(self.point_left_label)
        # ================================================
        
        # 字符“列”
        self.file_col_label = QLabel("列：",self)
        self.file_col_label.resize(QSize(208, 30))
        self.file_col_label.setFont(self.plain_font_size)
        # file_col_label.move(245+115+71,line3)
        # ================================================

        # 输入行位置
        self.input_box_row = QLineEdit(None,self)
        self.input_box_row.resize(45, 30)
        # self.input_box_row.move(195+115+71,line3)
        self.input_box_row.setFont(self.plain_font_size)
        self.line5_left.addWidget(self.input_box_row)
        # ================================================

        self.line5_left.addWidget(self.file_col_label)
        # 输入列位置
        self.input_box_col = QLineEdit(None,self)
        self.input_box_col.resize(45, 30)
        # self.input_box_col.move(270+115+71, line3)
        self.input_box_col.setFont(self.plain_font_size)
        self.line5_left.addWidget(self.input_box_col)
        # ================================================

        self.plus_font = QFont()
        self.plus_font.setPointSize(25)

        # 添加点
        self.add_point_button = QPushButton("+",self)
        self.add_point_button.setToolTip('<b>添加</b>当前输入的数据')
        self.add_point_button.resize(50, 30)
        # add_point_button.move(335+115+71, line3)
        self.add_point_button.setStyleSheet(r"border-radius:8px; font-size:35; border: 1px solid #84818C")
        self.add_point_button.clicked.connect(self.add_point)
        self.add_point_button.setFont(self.plus_font)
        self.line5_right.addWidget(self.add_point_button)
        # ================================================

        # 删除点
        self.del_point_button = QPushButton("-",self)
        self.del_point_button.setToolTip('<b>删除</b>最后输入的数据')
        # del_point_button.move(400+115+71, line3)
        self.del_point_button.resize(50, 30)
        self.del_point_button.setStyleSheet(r"border-radius:8px; background-color:#FFE061; font-size:35; border: 1px solid #84818C")
        self.del_point_button.clicked.connect(self.del_point)
        self.del_point_button.setFont(self.plus_font)
        self.line5_right.addWidget(self.del_point_button)

        # =================================================
        
        # 复制部分
        # line35 = line3 + linegap + 8
        # 输入随机数下限的标签
        self.line6 = QHBoxLayout()
        self.vbox.addLayout(self.line6)

        self.line6_left = QHBoxLayout()
        self.line6_right = QHBoxLayout()
        self.empty_line6 = QLabel()

        self.line6.addLayout(self.line6_left,5)
        self.line6.addLayout(self.line6_right,2)
        self.line6.addWidget(self.empty_line6,5)

        self.random_left_label = QLabel("请输入需要随机数下限：", self)
        self.random_left_label.resize(QSize(229, 30))
        self.random_left_label.setFont(self.plain_font_size)
        self.line6_left.addWidget(self.random_left_label)
        # random_left_label.move(55, line35)
        # ================================================
        
        # 字符“上限”
        self.random_right_label = QLabel("上限:",self)
        self.random_right_label.resize(QSize(48, 30))
        self.random_right_label.setFont(self.plain_font_size)
        
        # random_right_label.move(245,line35)
        # ================================================

        # 输入下限位置
        self.input_random_left = QLineEdit(None,self)
        self.input_random_left.resize(45, 30)
        # self.input_random_left.move(195, line35)
        self.input_random_left.setFont(self.plain_font_size)
        self.line6_left.addWidget(self.input_random_left)
        # ================================================

        # 输入上限位置
        self.input_random_right = QLineEdit(None,self)
        self.input_random_right.resize(45, 30)
        # self.input_random_right.move(282, line35)
        self.input_random_right.setFont(self.plain_font_size)
        
        self.line6_left.addWidget(self.random_right_label)

        self.line6_left.addWidget(self.input_random_right)
        # ================================================

        # 添加点
        self.add_random_button = QPushButton("+", self)
        self.add_random_button.setToolTip('<b>添加</b>一个随机数范围')
        self.add_random_button.resize(50, 30)
        # add_random_button.move(335, line35)
        self.add_random_button.setStyleSheet(r"border-radius:8px; font-size:35; border: 1px solid #84818C")
        self.add_random_button.clicked.connect(self.add_random)
        self.add_random_button.setFont(self.plus_font)
        self.line6_right.addWidget(self.add_random_button)
        # ================================================

        # 删除点
        self.del_random_button = QPushButton("-", self)
        self.del_random_button.setToolTip('<b>删除</b>一个随机数范围')
        # del_random_button.move(400,line35)
        self.del_random_button.resize(50,30)
        self.del_random_button.setStyleSheet(r"border-radius:8px; background-color:#FFE061; font-size:35; border: 1px solid #84818C")
        self.del_random_button.clicked.connect(self.del_random)
        self.del_random_button.setFont(self.plus_font)
        self.line6_right.addWidget(self.del_random_button)
        # =================================================
        # line4 = line3+ linegap + 50
        # line5 = line4
        # 显示所有的点
        self.line7 = QHBoxLayout()
        self.vbox.addLayout(self.line7)

        self.points_show_area_label = QLabel("已经选择的点（行，列）",self)
        self.points_show_area_label.resize(QSize(229, 30))
        # points_show_area_label.move(line_start_pos-37,line4)
        self.points_show_area_label.setFont(self.plain_font_size)
        self.line7.addWidget(self.points_show_area_label)
        
        self.show_area_layout = QHBoxLayout()
        self.vbox.addLayout(self.show_area_layout)

        self.points_show_area = QListWidget(self)
        # self.points_show_area.move(line_start_pos-45, line5+35)
        self.points_show_area.resize(150,150)
        self.points_show_area.setFont(self.plain_font_size)
        self.show_area_layout.addWidget(self.points_show_area)

        # 显示所有的随机数
        self.randoms_show_area_label = QLabel("已经选择的随机数", self)
        self.randoms_show_area_label.resize(QSize(166, 30))
        # randoms_show_area_label.move(line_start_pos+145,line4)
        self.randoms_show_area_label.setFont(self.plain_font_size)
        self.line7.addWidget(self.randoms_show_area_label)

        self.randoms_show_area = QListWidget(self)
        # self.randoms_show_area.move(line_start_pos+120,line5+35)
        self.randoms_show_area.resize(150, 150)
        self.randoms_show_area.setFont(self.plain_font_size)
        self.show_area_layout.addWidget(self.randoms_show_area)

        # 数据显示窗口
        self.data_show_area_label = QLabel("对应Block的数据",self)
        self.data_show_area_label.resize(QSize(158, 30))
        # data_show_area_label.move(502, line4)
        self.data_show_area_label.setFont(self.plain_font_size)
        self.line7.addWidget(self.data_show_area_label)

        self.data_show_area = QTextEdit(None, self)
        self.data_show_area.resize(365, 150)
        # self.data_show_area.move(line_start_pos+298,line5+35)
        self.data_show_area.setReadOnly(True)
        self.data_show_area.setFont(self.plain_font_size)
        self.show_area_layout.addWidget(self.data_show_area)


        # SPECIAL LAYOUT
        # 计算用的按钮
        self.last_box = QHBoxLayout()
        self.left_last_box = QVBoxLayout()

        self.last_box.addLayout(self.left_last_box)

        self.last_empty_label = QLabel('')
        self.last_box.addWidget(self.last_empty_label)

        self.last_box.setStretchFactor(self.left_last_box,1)
        self.last_box.setStretchFactor(self.last_empty_label,3)

        self.vbox.addLayout(self.last_box)
        
        self.generate_button_font = QFont()
        self.generate_button_font.setPointSize(16)
        
        self.del_all_font = QFont()
        self.del_all_font.setPointSize(16)
        # 清空数据
        self.del_all_button = QPushButton("清空输入", self)
        self.del_all_button.setToolTip('<b>删除所有指定的点数据</b>')
        self.del_all_button.resize(QSize(94, 35))
        self.del_all_button.setFont(self.del_all_font)
        self.del_all_button.setStyleSheet("background-color:red; color: white")
        # del_all_button.move(125-85 ,422)
        self.del_all_button.clicked.connect(self.clearall)
        self.left_last_box.addWidget(self.del_all_button)
        # =================================================

        self.btn = QPushButton("生成文件", self)
        self.btn.setToolTip('<b>确认无误后</b>按下此按钮生成文件.')
        self.btn.resize(120, 68)
        # btn.move(472, 426)
        self.btn.setFont(self.generate_button_font)
        self.btn.clicked.connect(self.save_file)

        # 传输文件的按钮
        self.transmit_button = QPushButton("传输至SAS",self)
        self.transmit_button.setToolTip('<b>确认无误后传输文件到SAS</b>')
        self.transmit_button.resize(120,68)
        # transmit_button.move(613, 426)
        self.transmit_button.clicked.connect(self.transmit_file)
        self.transmit_button.setFont(self.generate_button_font)
        
        self.advanced_setting_button = QPushButton("高级", self)
        self.advanced_setting_button.setToolTip('设置SAS文件路径')
        self.advanced_setting_button.resize(QSize(68,35))
        # self.advanced_setting_button.move(50, 463)
        self.advanced_setting_button.setFont(self.plain_font_size)
        self.left_last_box.addWidget(self.advanced_setting_button)

        self.last_box.addWidget(self.btn)
        self.last_box.addWidget(self.transmit_button)
        self.vbox.setStretchFactor(self.last_box,2)

        self.show_complement_info()        
        # 窗口部分设置
        self.setGeometry(238,118,749,617)
        self.setWindowTitle("随机数替换")
        self.setLayout(self.vbox)
        self.show()
        self.writelog(5, 'UI Layout Set, Ready to go')

    def file_browser_action(self):
        browsed_path = QFileDialog.getOpenFileUrl(self, "Browser", ".")
        this_path = browsed_path[0].toLocalFile()
        this_path.replace(r'file://','')
        self.file_position_input_box.setText(this_path)
        self.show_data()

    def show_complement_info(self):
        info_type = self.random_number_type[self.random_function_choose_list.currentText()]
        # initiated when the element of
        self.complement_label_a.hide()
        self.complement_label_gamma.hide()
        self.complement_first_insert.hide()
        self.complement_label_b.hide()
        self.complement_second_insert.hide()
        self.complement_label_c.hide()
        self.complement_third_insert.hide()
        self.input_random_right.setReadOnly(False)
        self.input_random_left.setReadOnly(False)
        self.input_random_right.setStyleSheet("background-color:#FFFFFF")
        self.input_random_left.setStyleSheet("background-color:#FFFFFF")
        self.input_random_right.setText("")
        self.input_random_left.setText("")

        if info_type == 1:
            self.random_explain_label.setText("Uniform Distribution")
        
        if info_type == 0:
            self.random_explain_label.setText("Gaussian Distribution")

        if info_type == 2 : # 指数
            self.complement_label_gamma.show()
            self.complement_first_insert.show()
            self.random_explain_label.setText(
                "Expotential Distribution: f(x)=γe^(-γ*x)")
            self.input_random_left.setText("NULL")
            self.input_random_right.setText("NULL")
            self.input_random_right.setReadOnly(True)
            self.input_random_left.setReadOnly(True)
            self.input_random_right.setStyleSheet("background-color:#CCCCCC")
            self.input_random_left.setStyleSheet("background-color:#CCCCCC")
       
        if info_type == 3: # 二次函数
            self.complement_label_a.show()
            self.complement_first_insert.show()
            self.complement_label_b.show()
            self.complement_second_insert.show()
            self.complement_label_c.show()
            self.complement_third_insert.show()
            self.random_explain_label.setText("Quadratic Distribution: f(x)=ax^2+bx+c")

    def add_point(self):
        # 保证数据不能重复
        if self.input_box_row.text() and self.input_box_col.text() and self.block_name_input.text():
            point = (self.block_name_input.text(),int(self.block_insert.text() or 1),int(self.input_box_row.text()), int(self.input_box_col.text()))
            if point not in self.selected_points:
                self.selected_points.append(point)
                self.points_show_area.addItem("{}-{}: ({},{})".format(*point))
            self.input_box_row.clear()
            self.input_box_col.clear()
            self.writelog(6, 'Input point:({},{})'.format(point[0],point[1]))
        # 添加能够 显示数据 的功能

    def del_point(self):
        if len(self.selected_points):
            current = self.points_show_area.currentRow()
            if current == -1:
                return
            itemdeleted = copy(self.selected_points[current])
            self.points_show_area.takeItem(current)
            del self.selected_points[current]
            self.writelog(7, 'Point deleted:({},{})'.format(itemdeleted[0],itemdeleted[1]))
            itemdeleted = None

    def add_random(self):
        if self.input_random_right.text() and self.input_random_left.text() and len(self.selected_points) > len(self.selected_randoms):
            random_type_name = self.random_function_choose_list.currentText()
            random_type = self.random_number_type[random_type_name]
            show_area_sentence = ''
            
            if random_type < 2:
                try :
                    point = (float(self.input_random_left.text()),float(self.input_random_right.text()))
                except :
                    QMessageBox.warning(self,"警告",'不合法的输入',QMessageBox.Ok)
                    return
                show_area_sentence = "({},{}),{}".format(*point,random_type_name)
            if random_type == 2:
                # expotential
                # 用上限开刀，上限是列表，中间有参数
                # point = (float(self.input_random_left.text()),[float(self.input_random_right.text())])
                point = (0,[0])
                gamma_num = float(self.complement_first_insert.text() or 1)
                if gamma_num == 0.0 or gamma_num == 0:
                    QMessageBox.warning(self, "警告", 'γ不能为0',QMessageBox.Ok)
                    return
                point[1].append(gamma_num)
                show_area_sentence = "γ={},exp".format(*point[1][1:])

            if random_type == 3:
                point = (float(self.input_random_left.text()), [float(self.input_random_right.text())])
                point[1].extend([float(self.complement_first_insert.text() or 0),float(self.complement_second_insert.text() or 0),float(self.complement_third_insert.text() or 0)])
                show_area_sentence = "a={},b={},c={},quad".format(*point[1][1:])
            if show_area_sentence:
                self.randoms_show_area.addItem(show_area_sentence)
            self.selected_randoms.append(point)
            self.random_type_list.append(random_type)
            self.input_random_left.clear()
            self.input_random_right.clear()
            self.writelog(6, 'Random range added:({},{})'.format(*point))

    def del_random(self):
        # random_type_list
        # randoms_show_area
        # selected_randoms
        if len(self.selected_randoms):
            current = self.randoms_show_area.currentRow()
            if current == -1:
                return
            itemdeleted = copy(self.selected_randoms[current])
            self.randoms_show_area.takeItem(current)
            del self.selected_randoms[current]
            del self.random_type_list[current]
            self.writelog(7, 'Random range deleted:({},{})'.format(*itemdeleted))
            itemdeleted = None

    def show_data(self):
        block_str = ''
        if not self.file_position_input_box.text():
            QMessageBox.warning(self,'警告','请填入合理的文件位置',QMessageBox.Ok)
            self.writelog(2,'Empty File Path')
        else :
            path = self.file_position_input_box.text()
            try :
                f = analyzedataset.LoadFile(path)
            except :
                QMessageBox.warning(self,'警告','文件不存在或已经损坏，请填写正确的位置')
                self.writelog(2,'Invalid Path Detected at:{}'.format(self.file_position_input_box.text()))
                return
            if f.hasContext:
                if self.block_name_input.text():
                    try:
                        block_num = int(self.block_insert.text())
                        b = self.block_name_input.text()
                        if b in f.blocks:
                            # 可以添加block的序号
                            for count, data_block in enumerate(f[b]):
                                if count + 1 == block_num:
                                    block_str += "block name: {} Channel:{}\n".format(
                                        b, count+1)
                                    for row in data_block:
                                        block_str += row['rawline'] + '\n'
                                    block_str += '='*30 + '\n\n'

                            self.writelog(
                                3, 'Showing All Data in Block:{}'.format(b))
                        else:
                            block_str = "不存在的block"
                            self.writelog(
                                2, 'Invalid Block Input:{}'.format(b))
                    except:
                        if not self.block_insert.text():
                            self.writelog(2,'Invalid Block Channel Input')
                        b = self.block_name_input.text()
                        if b in f.blocks:
                            # 可以添加block的序号
                            for count, data_block in enumerate(f[b]):
                                block_str += "block name: {} Channel:{}\n".format(b,count+1)
                                for row in data_block:
                                    block_str += row['rawline'] + '\n'
                                block_str += '='*30 + '\n\n'
                            self.writelog(3,'Showing All Data in Block:{}'.format(b))
                        else :
                            block_str = "不存在的block"
                            self.writelog(2,'Invalid Block Input:{}'.format(b))

                else :
                    # block 为空，输出所有的block
                    block_str = '您没有输入block，下面的Block可以供参考\n' + ' '.join(set(f.blocks))
                    block_str += '\n' + '='*30 + '\n'
                    block_str += '原始数据: \n'
                    block_str += '\n'.join(f.row_list)
                    self.writelog(3,'Showing the whole file {}'.format(path))
            else :
                block_str = '文件已经损坏或无法打开，请检查文件名是否输入正确'
                self.writelog(1,'Error when reading file at path {}'.format(path))
        self.data_show_area.setText(block_str)


    def clearall(self):
        if QMessageBox.warning(self, '确认', '确定要清空?', QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
            self.block_name_input.clear()
            self.block_insert.clear()
            self.input_box_row.clear()
            self.input_box_col.clear()
            self.points_show_area.clear()
            self.random_type_list = []
            self.randoms_show_area.clear()
            self.number_of_randoms_input.clear()
            self.selected_points = []
            self.selected_randoms = []
            self.writelog(2,'CLEAR ALL')

    def save_file(self):
        self.writelog(4,'Trying to generate files...')
        if not len(self.selected_points) == len(self.selected_randoms):
            QMessageBox.warning(self,'警告','随机数的范围没有完全指定')
            self.writelog(2,'Number of random numbers and points are not equal.')
            self.writelog(4,'Generating Process Aborted.')
            return
        if not self.file_position_input_box.text():
            QMessageBox.warning(self,'警告','请填入合理的文件位置',QMessageBox.Ok)
            self.writelog(
                2, 'Empty File Path')
            self.writelog(4, 'Generating Process Aborted.')
            return
        try :
            f = analyzedataset.LoadFile(self.file_position_input_box.text())
        except :
            QMessageBox.warning(self,'警告','输入的文件无法打开',QMessageBox.Ok)
            self.writelog(1, 'Error when reading file at path {}'.format(path))
            self.writelog(4, 'Generating Process Aborted.')
            return

        if not f.hasContext:
            QMessageBox.warning(self,'警告','文件位置输入不正确或文件已损坏',QMessageBox.Ok)
            self.writelog(1, 'Error when reading file at path {}'.format(path))
            self.writelog(4, 'Generating Process Aborted.')
            return

        try :
            number_of_randoms = int(self.number_of_randoms_input.text())
        except :
            QMessageBox.warning(self,'警告','请输入随机数个数', QMessageBox.Ok)
            self.writelog(2, 'Number of random numbers are not detected.')
            self.writelog(4, 'Generating Process Aborted.')
            return
        # check if all number are valid
        try :
            for point in self.selected_points :
                msg = ''
                # point: block - block编号 - 行 - 列
                block_position = index_by_times(f.blocks,point[0],point[1])
                if block_position == -1:
                    msg = '发现block没有出现在文件中'
                    self.writelog(2, 'Invalid Block Input:{}'.format(b))
                    self.writelog(4, 'Generating Process Aborted')
                    raise KeyError
                this_block_lines = f.data_per_block[block_position]
                this_block_rows = [i['row'] for i in this_block_lines]
                try :
                    row_position = this_block_rows.index(point[2])
                except :
                    msg = '行号超出范围'
                    self.writelog(
                        2, 'Invalid Row Position:{}'.format(row_position))
                    self.writelog(4, 'Generating Process Aborted')
                    raise KeyError
                if point[3] > this_block_lines[row_position]['count']:
                    msg = '列号超出范围'
                    self.writelog(
                        2, 'Invalid Col Position:{}'.format(point[3]))
                    self.writelog(4, 'Generating Process Aborted')
                    raise KeyError

        except Exception as e :
            # print(e)
            if msg:
                QMessageBox.warning(
                    self, '警告', '{}\n请检查block和位置的输入是否合理'.format(msg), QMessageBox.Ok)
            else :
                self.writelog(1,'Unknown Error Detected.')
                self.writelog(4,'Generating Process Aborted')
                QMessageBox.warning(
                    self, '警告', '未知错误\n请检查block和位置的输入是否合理'.format(msg), 
                    QMessageBox.Ok)
            return

        try :
            number_of_randoms = int(self.number_of_randoms_input.text())
        except :
            QMessageBox.warning(self,'警告','请输入合理的随机数个数',QMessageBox.Ok)
            self.writelog(2,'Invalid Number of Randoms Input:{}'.format(self.number_of_randoms_input.text()))
            self.writelog(4,'Generating Process Aborted')
            return

        path_initial = os.path.dirname(self.file_position_input_box.text())
        folder_count = 1
        self.writelog(4,'CHECK COMPLETE!')
        self.path_initial = path_initial
        while(True):
            folder_path = os.path.join(path_initial,'{}'.format(folder_count))
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
                self.current_folder = folder_path
                break
            folder_count += 1
        self.writelog(4,'Files would be located in {}'.format(folder_path))


        for filecount, to_be_alterred_numbers in enumerate(alterdata.yield_dataset(self.selected_randoms,self.random_type_list,number_of_randoms)):
            # 注意: 随机数已经取得，正在变更数据
            data_for_change = deepcopy(f.data_per_block) # list of dicts
            for count,point in enumerate(self.selected_points) :
            # block名字 - block序号 行号 列号
                block_index = index_by_times(f.blocks,point[0],point[1])
                this_block_rows = [i['row'] for i in data_for_change[block_index]]
                row_index = this_block_rows.index(point[2])
                # print(data_for_change[block_index][row_index])

                data_for_change[block_index][row_index]['data'][point[3]-1] = to_be_alterred_numbers[count]
            # data_for_change已经更改完毕
            # data_for_change和blocks等等一起可以进行文件拼写
            # 注意format格式
            # 从header开始
            str_to_be_written = '\n'.join(f.header) + '\n'
            # block_header_notion block的开头样式，直接添加即可
            for count,b in enumerate(data_for_change) :
                # b: 一个block已经更改了的数据
                str_to_be_written += f.block_header_notion[count] + '\n'
                for line_count, line_dict in enumerate(f.data_per_block[count]) :
                    str_to_be_written += line_dict['rawline'][:12] + alterdata.data_append(b[line_count]['data'],line_dict['length']) + '\n'
                str_to_be_written += '    -1\n'
            str_to_be_written += f.endjob_notion

            file_final_path = os.path.join(folder_path,'{}.inp'.format(filecount))
            with open(file_final_path,'w') as file_to_be_written:
                file_to_be_written.write(str_to_be_written)
            # write/save to file
        self.didGenerateFiles = True
        self.current_folder_file_count = filecount # 生成文件数
        self.writelog(4,'{} files are written.'.format(filecount+1))
        self.writelog(4,'Generating Process Complete!')
    
    def transmit_file(self):
        self.writelog(8,'Transmitting process begin...')
        print('传输开始')        
        if THIS_SYSTEM == 'OTHERS':
            QMessageBox.warning(self, '错误', '系统错误，未知的系统', QMessageBox.Ok)
            self.writelog(1,'Unexpected system platform')
            self.writelog(1,'FATAL ERROR: Files can\'t be sent')
            self.writelog(8,'Transmitting process ABORTED')
            return
        if not self.didGenerateFiles:
            QMessageBox.warning(self, '警告', '尚未生成文件', QMessageBox.Ok)
            self.writelog(2,'Sending files before generating')
            self.writelog(8,'Transmitting process ABORTED') 
            return
        # 创建文件夹

        self.writelog(8,'Before Transmitting Checklist Complete!')

        print('自检完成')
        self.clear_previous()

        result_count = 1
        while True:
            result_path = self.current_folder + '_result'
            if result_count != 1:
                result_path = result_path + str(result_count)
            if not os.path.exists(result_path):
                os.mkdir(result_path)
                self.result_path_full = result_path
                break
        # 文件夹创建完毕
        print('文件夹创建完成')
        # 获取输入输出文件名
        input_file_form = os.path.join(self.current_folder,'{}.inp')
        output_file_form = os.path.join(self.result_path_full,'{}.out')
        # 获取完毕
        print('文件总数：{}'.format(self.current_folder_file_count))
        # 循环开始
        # thread1 = multiprocessing.Process() # PlaceHolder
        # thread2 = multiprocessing.Process()
        for i in range(self.current_folder_file_count + 1):
            # if i:
                # thread1.terminate();thread2.terminate()
            self.squawk = 0
            total_time_per = self.info_list[1] - self.interval
            self.writelog(8,'Sending {}.inp...'.format(i))
            print('Doing {} to {}'.format(
                input_file_form.format(i), output_file_form.format(i)))
            
            if __name__ == "__main__":
                thread1 = WorkingThread(self.info_list[0], input_file_form.format(i), output_file_form.format(i))
                thread1.start()
            time.sleep(self.interval)
            print('程序睡眠{}秒'.format(self.interval))
            try:
                with open('SAS.pid') as f:
                    content = f.readlines()
                pid_raw = content[0].strip().split()
                self.squawk = int(pid_raw[1])
                print('PID已经取得')
            except:
                pass
            while thread1.is_alive() and total_time_per >= 0:
                time.sleep(1)
                total_time_per -= 1
            if total_time_per < 0:
                self.window.writelog(8, '<ERROR> {}.inp transmission TIME OUT!'.format(self.inputNum))
                if THIS_SYSTEM == 'WINDOWS':
                    os.system('taskkill.exe /pid:'+str(self.squawk))
                if THIS_SYSTEM == 'MACOS':
                    os.system('kill {}'.format(self.squawk))
                print('WorkingThread Killed.')

            self.clear_previous()
        # 循环体成功退出，注意记录
        # 函数结束
        self.didGenerateFiles = False

        

    def closeEvent(self,event):
        self.logfile.write(time.strftime('\n<END>   System ends at %Y-%m-%d %H:%M:%S   TIMEZONE: %z', time.localtime(time.time())))
        event.accept()

if __name__ == "__main__":
    log_file_name = time.strftime("LOG_%y%m%d_%H%M%S.txt",time.localtime(time.time()))
    log_file = open(log_file_name,'w')
    log_file.write(time.strftime("<START> System starts at %Y-%m-%d %H:%M:%S TIMEZONE:%z", time.localtime(time.time())))
    log_file.write('\n\n')
    app = QApplication(sys.argv)
    w = Window(sys.argv + [log_file])
    ad_w = advance_view(w.info_list)
    w.advanced_setting_button.clicked.connect(ad_w.handle_click)
    sys.exit(app.exec_())


