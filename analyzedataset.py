#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

from copy import deepcopy
import sys

'''
LOG: 20180608
在数据结构中加入通道CHANNEL的部分，数组处理
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
        # data_per_block是一个列表 data_per_block -> 每个list表示一个block的所有数字 -> list中的字典表示一行数据
        # 不通过字典的形式 改成list
        # 声明私有&只读变量
        self.__sep = sep

        # 完整的读入文档
        # try :
        f = open(path,'r')
        self.row_list = [line.rstrip() for line in f.readlines()]
        self.hasContext = True
        self.splitBlocks()
        '''
        except Exception as e :
            print(e)
            self.row_list = "文件无法打开，请检查路径是否正确"
            self.hasContext = False
        '''

    @property
    def sep(self):
        return self.__sep


    def splitBlocks(self):
        # 结构：data_per_block 的每个列表是一个block的所有元素
        self.header = self.row_list[:3]
        data_without_header = deepcopy(self.row_list[3:])
        for line_total in data_without_header :
            # No in-place changes are allowed.
            line_total.rstrip()
            if self.__sep == ' ' :
                line = line_total.split()
            else :
                line = line_total.split(self.__sep)
            if not line[0].isdigit(): # 包括了-1和字母
                if not '-1' in line[0]:
                    # block的开头
                    if 'ENDJOB' in line[0] :
                        self.endjob_notion = line_total
                        continue
                    self.blocks.append(line[0])
                    self.block_header_notion.append(line_total)
                    self.block_channel.append(int(line[2]))
                    this_block = [] # 清空block
                    # line:元素个数 line_total:总长度

                else :
                    # 发现了-1，一个block已经解析完毕
                    self.data_per_block.append(this_block)
                    
            else :
                # 数字
                # 解析黏连的数据 从1开始（第二个数字就要开始

                # 防止第一个数就出现问题
                number_of_numbers = int(line_total[6:12])
                if len(line[1])>6 :
                    item2 = line[1][number_of_numbers :]
                    item1 = str(number_of_numbers)
                    line[1] = item1
                    line.insert(2,item2)

                '''
                try :
                    number_of_numbers = int(line[1])
                except :
                    # insert 向左！ fuck
                    data = line[1]
                    line[1] = data[:1]
                    line.insert(2,data[1:])
                    line_total = ' '.join(line)

                number_of_numbers = int(line[1])

                # 方案二，能够防止第一个数出问题而且数据数量大于10，待完善，目前不用
                if number_of_numbers > 99 :
                    data = line[1]
                    line[1] = data[:1]
                    line.insert(2,data[1:])
                    line_total = ' '.join(line)
                '''
# 注意数据第一个就黏连会导致line_total 的长度和预期不同
                position1 = line_total.index(line[0]) + len(line[0])
                # position1指向第二个元素开始的第一个
                position2 = line_total[position1:].index(line[1]) + len(line[1])
                length_of_data = len(line_total) - position2 - position1
                this_block_length = int(length_of_data / number_of_numbers)
                for i in range(2,number_of_numbers+2):
                    if len(line[i]) > this_block_length:
                        # 需要拆开
                        item1 = line[i][: -this_block_length]
                        item2 = line[i][-this_block_length:]
                        line[i] = item1
                        line.insert(i+1,item2)


                block_datas = {'row':int(line[0]),'count':int(number_of_numbers),'data':[float(line[i+2].replace('D','E'))  for i in range(int(number_of_numbers))] if int(number_of_numbers)!=0 else [],'rawline':line_total,'length':this_block_length} # block_datas 一行的数字
                this_block.append(block_datas)
                

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
    path = "/Users/wangtianmin/Downloads/test.inp"
    ins = LoadFile(path)
    print(ins.hasContext)
    if ins.hasContext:
        print(ins['COOLIN'])
        print(list(zip(ins.blocks,ins.block_channel)))
if __name__ == "__main__":
    main()


