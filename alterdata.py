#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise
import numpy as np

def genpl(itembound=(0,4),number=2):
    '''
    程序要用到的内置函数
    一个合格的枚举器
    '''
    l = [itembound[0],] * number
    l[-1] -= 1
    for i in range((itembound[1]-itembound[0]+1) ** number):
        l[-1] += 1
        # re-arrange 进位
        a=list(range(1,number))
        a.reverse()
        for i in a:
            # a-1 available
            if(l[i]>itembound[1]):
                l[i-1] += 1
                l[i] -= (itembound[1]-itembound[0])+1
        yield l

def yield_dataset(random_ranges,random_type,number_of_randoms):
    random_data_set = [] # 每个元素 表示一个空格需要取的所有随机数
    number_of_numbers = len(random_ranges)
    for i in range(number_of_numbers):
        # 检测随机数的上下界
        random_range_lower, random_range_higher = random_ranges[i]
        if random_range_lower > random_range_higher:
            buff = random_range_lower
            random_range_lower = random_range_higher
            random_range_higher = buff
        if random_type == 1 :
            # 1为均匀分布 0为高斯分布 可以添加
            random_numbers = np.random.rand(number_of_randoms)*(random_range_higher - random_range_lower) + random_range_lower
        if random_type == 0 :
            mu = (random_range_higher + random_range_lower) / 2
            sigma = ((random_range_higher - random_range_lower) / 2) / 2.576 # 99%置信区间
            random_numbers = np.random.randn(number_of_randoms)*sigma+mu

        random_data_set.append(random_numbers)
    ite = genpl(itembound=(0,number_of_randoms-1), number = number_of_numbers)
    for xh in ite:
        randoms_to_be_yielded = []
        for i in range(number_of_numbers) :
            randoms_to_be_yielded.append(random_data_set[i][xh[i]])
        yield randoms_to_be_yielded

def data_append(data,length):
    s = ''
    for num in data:
        data_str = ('{:%dg}'%length).format(num)
        if len(data_str) > length:
            if 'E' in data_str or 'e' in data_str:
                # 1.0000000E+12 length = 6
                if 'E' in data_str:
                    e_position = data_str.index('E')
                else :
                    e_position = data_str.index('e')
                length_without_e = len(data_str) - e_position
                data_str = data_str[:length_without_e] + data_str[e_position:]
            else :
                data_str = data_str[:length]
        s += data_str
    return s


def main():
    print('     1     4' + data_append([133333333333333333],6))

if __name__ == "__main__":
    main()


