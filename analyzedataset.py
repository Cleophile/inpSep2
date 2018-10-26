#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

from copy import deepcopy
import sys

'''
LOG: 20180608
在数据结构中加入通道CHANNEL的部分，数组处理
空格分割优先
INPCOM     1     1     0 第二个数字：channel 
BLOCK后面数字的含义
可能修改一下索引的语法
可能也需要更改图形界面的效果
批次处理

Profile: 加和的值的变化，改变整个profile的值（NUMPY直接批处理
增加项：Profile 的位置，添加isProfile，改变profile的值时候统一改变总体的值

增加日志，增加log的内容

批处理：执行不下去的时候自动跳过（log xxx.exe ...）
get: prompt stderr info
报错新建log
'''

'''
LOG_FILE的内容：
    1. try except部分：except的内容需要详细写在log的内容中
    2. 用户选择了哪些内容
    log的内容分3个部分：
    <START> 注明程序开始的时间
    <END> 注明程序关闭的时间
    <1> [ERROR] 导致某个操作无法完成的错误
    <2> [WARNING] 比如被系统识别的输出错误
    <3> [SEARCH] 用户搜索的记录
    <4> [GENERATE] 新增了某项内容
    <5> [SYSTEM] 系统报告
    <6> [INPUT] 用户输入
    <7> [DEL] 用户删除
'''

class LoadFile(object):
    '''
    用于读取文件的类
    blocks: 所有的模块
    '''
    def __init__(self,path,sep=' '):
        self.path_initial_file = path
        self.blocks = []
        self.block_channel = []
        self.data_per_block = []
        self.block_header_notion = []
        self.in_xnote = False
        # data_per_block是一个列表 data_per_block -> 每个list表示一个block的所有数字 -> list中的字典表示一行数据
        # 不通过字典的形式 改成list
        # 声明私有&只读变量
        self.__sep = sep

        # 完整的读入文档
        try :
            f = open(path,'r')
            content = f.readlines()
        # Fuck Away Comments:
        except :
            f = open(path,'r',encoding='GB18030')
            content = f.readlines()
        cleaned_dta = []
        for i in content:
            cleaned_dta.append(i.split('#')[0])
        cleaned_dta = [i for i in cleaned_dta if i]
        # Comments Gone
        self.row_list = [line.rstrip() for line in cleaned_dta]
        self.hasContext = True
        self.splitBlocks()

    @property
    def sep(self):
        return self.__sep

    def splitBlocks(self):
        # 结构：data_per_block 的每个列表是一个block的所有元素
        self.header = self.row_list[:3]
        data_without_header = deepcopy(self.row_list[3:])
        this_block = []
        for line_total in data_without_header :
            # No in-place changes are allowed.
            # line_total.rstrip()
            if self.__sep == ' ' :
                line = line_total.split()
            else :
                line = line_total.split(self.__sep)
            if len(line) == 0:
                block_datas = {'tail_position': 0, 'row': -1, 'count': 0, 'data': [], 'rawline': line_total, 'length': 0, 'iscomment': True}
                continue
            if not line[0].isdigit(): # 包括了-1和字母
                if not '-1' in line[0]:
                    if self.in_xnote:
                        block_datas = {'tail_position': 0, 'row':-1, 'count': 0, 'data': [], 'rawline': line_total, 'length': 0, 'iscomment': True}
                        this_block.append(block_datas)
                        continue
                    # block的开头
                    if 'ENDJOB' in line[0] :
                        self.endjob_notion = line_total
                        continue
                    self.blocks.append(line[0])
                    self.block_header_notion.append(line_total)
                    try:
                        self.block_channel.append(int(line[2]))
                    except:
                        self.in_xnote = True
                        self.block_channel.append(-1)
                    this_block = [] # 清空block
                    # line:元素个数 line_total:总长度

                else :
                    # 发现了-1，一个block已经解析完毕
                    self.data_per_block.append(this_block)
                    self.in_xnote = False
                    
            else :
                # 数字
                # 解析黏连的数据 从1开始（第二个数字就要开始
                # 防止第一个数就出现问题
                # 思路：在最后一个数据地方添加一个assert？
                
                simple_worked = False
                
                try:
                    data_this_line = []
                    # 空格的解析, 这是最最原始的方法，但是需要很多很多个assert条件，比较严格
                    # 这不是完全的，需要在最后进行进一步的assert，comment的内容需要全部打印出来
                    # 解析失败的数据利用comment来表示
                    number_of_numbers = int(line_total[6:12])
                    comment = ' '.join(line[2+number_of_numbers:])
                    this_line_position = [6, 12]  # 结束为止
                    for i in range(number_of_numbers):
                        data_this_line.append(float(line[2+i].replace('D','E')))
                        this_line_position.append(line_total[this_line_position[-1]:].index(
                            line[2+i]) + len(line[2+i]) + this_line_position[-1])
                    if len(line) != number_of_numbers + 2:
                        tail_position = line_total[this_line_position[-1]:].index(line[2+number_of_numbers
                                                                                    ]) + this_line_position[-1]
                    else:
                        tail_position = len(line_total) - 1
                    this_block_length = (this_line_position[-1] - 12) // number_of_numbers
                    if number_of_numbers * this_block_length + 12 < this_line_position[-1]:
                        this_block_length += 1

                    block_datas = {'tail_position': tail_position, 'row': int(
                        line[0]), 'count': number_of_numbers, 'data': data_this_line, 'rawline': line_total, 'length': this_block_length, 'iscomment': False}
                    this_block.append(block_datas)
                    # print(block_datas)
                    simple_worked = True

                except:
                    pass

                block_datas = None
                tail_position = None
                this_line_position = None
                data_this_line = []
                number_of_numbers = None
                this_block_length = None
                if simple_worked:
                    continue

                try :
                    number_of_numbers = int(line_total[6:12])
                except : # All comments
                    block_datas = {'tail_position': 0, 'row': int(line[0]), 'count': 0, 'data': [], 'rawline': line_total, 'length': 0, 'iscomment': True}
                first_item_length = len(str(number_of_numbers))
                if len(line[1])>first_item_length : # 第一个数字黏连
                    item2 = line[1][first_item_length:]
                    item1 = str(number_of_numbers)
                    line[1] = item1
                    line.insert(2,item2)

# 注意数据第一个就黏连会导致line_total 的长度和预期不同
                position1 = line_total[12:].index(line[2]) + 12
                position = [position1]
                for i in range(3, len(line)):
                    this_position = position[i-3] + len(line[i-1])
                    position.append(line_total[this_position:].index(line[i])+this_position)
                # 情况1：没有附加的信息，对于是否黏连的情况都有了考虑
                for i in range(number_of_numbers, 0, -1):
                    if i + 2 > len(line):
                        continue
                    length_of_all_data = position[i-1] + len(line[i+1]) - 12
                    this_block_length = length_of_all_data // number_of_numbers
                    if this_block_length * number_of_numbers != length_of_all_data:
                        continue
                    try:
                        data_this_line = []
                        for i in range(number_of_numbers):
                            data_this_line.append(float(
                                line_total[12+this_block_length*i: 12+this_block_length*(i+1)].replace('D', 'E')))
                        # block_datas 一行的数字
                        if len(position) <= i:
                            tail_position = -1
                        else:
                            tail_position = position[i]
                        block_datas = {'tail_position': tail_position, 'row': int(
                            line[0]), 'count': number_of_numbers, 'data': data_this_line, 'rawline': line_total, 'length': this_block_length, 'iscomment': False}
                        break
                    except:
                        pass
                else:
                    block_datas = {'tail_position':0, 'row': int(line[0]), 'count': 0, 'data': [], 'rawline': line_total, 'length': 0, 'iscomment': True}
                this_block.append(block_datas)
                # print(block_datas)


# 这里结构有点混乱 需要重新修改结构 确保data

    def getData(self):
        return deepcopy(self.row_list)

    def __getitem__(self, key):
        datas = []
        for count, block_name in enumerate(self.blocks):
            if block_name == key :
                datas.append(self.data_per_block[count])
        return datas

    

def main():
    path = '/Users/wangtianmin/WorkingMain/septxt_proj/cleaned_sample.inp'
    # path = "/Users/wangtianmin/Downloads/test.inp"
    ins = LoadFile(path)
    if ins.hasContext:
        pass
if __name__ == "__main__":
    main()


