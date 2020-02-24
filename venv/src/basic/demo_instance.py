#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cmath
import math
import search_utils
import sort_utils

#python数字求和
def demo_01_sum(intx, inty, *intz) :
    sum = intx + inty
    for i in intz:
        sum += i
    return sum

#求平方根
def demo_02_sqrt_root(num) :
    num_sqrt = num ** 0.5
    print('%0.3f 的平方根为 %0.3f' % (num, num_sqrt))
    #复数的平方根
    num_sqrt = cmath.sqrt(num)
    print('{0} 的平方根为 {1:0.3f}+{2:0.3f}j'.format(num ,num_sqrt.real,num_sqrt.imag))

#计算三角形的面积
def demo_03_triangle_area(a,b,c) :
    if (a > 0 and b > 0 and c > 0 and (a + b > c) and (a - b < c)) :
        #判断三角形的条件
        #海伦公式
        s = (a + b + c ) / 2 # 半周长
        area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
        print('三角形(%0.2f,%02.f,%0.2f)面积为 %0.2f' % (a,b,c,area))
        print('三角形({},{},{})面积为 {}'.format(a,b,c,area))
    else :
        print("输入的参数不是三角形！")

#计算圆的面积
def demo_04_circle_area(r) :
    area = math.pi * (r ** 2)
    print('半径为{}的圆面积为 {}'.format(r, area))

#计算指定范围内的素数
def demo_05_prime(lower, upper) :
    tuple = []
    for num in range(lower, upper) :
        for i in range(2,num) :
            if (num % i) == 0 :
                break
        else :
            tuple.append(num)
    print(tuple)

def is_numeric(str) :
    try:
        float(str)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(str)
        return True
    except (TypeError, ValueError):
        pass
    return False

def demo_06_numeric() :
    # 测试字符串和数字
    print(is_numeric('foo'))  # False
    print(is_numeric('1'))  # True
    print(is_numeric('1.3'))  # True
    print(is_numeric('-1.37'))  # True
    print(is_numeric('1e3'))  # True
    # 测试 Unicode
    print(is_numeric('٥'))  # 阿拉伯语 5
    print(is_numeric('๒'))  # 泰语 2
    print(is_numeric('四'))  # 中文数字
    print(is_numeric('©'))  # 版权号 False

def demo_07_multip_table() :
    # 九九乘法表
    for i in range(1, 10):
        for j in range(1, i + 1):
            print('{} x {} = {}\t'.format(j, i, i * j), end='')
        print()

def demo_08_narcissistic_number() :
    #水仙花数：水仙花数是指一个 3 位数，它的每个位上的数字的 3次幂之和等于它本身
    for num in range(100,1000) :
        i = num // 100   #百分位, 取整除 - 向下取接近除数的整数
        j = num // 10 % 10  # //地板除
        k = num % 10
        if num == i ** 3 + j ** 3 + k ** 3:
            print("水仙花数{},{},{},{}".format(i,j,k,num))

def demo_21_search_binary() :
    # 测试数组
    arr = [2, 3, 4, 10, 40]

    # 函数调用
    result, counter = search_utils.binary_search(arr, 0, len(arr) - 1, 10, 0)
    print("二分查找1：元素在数组中的索引为 %d, 查找次数为 %d" % (result, counter))
    result, counter = search_utils.binary_search2(arr, 10)
    print("二分查找1：元素在数组中的索引为 %d, 查找次数为 %d" % (result, counter))
    result, counter = search_utils.liner_search(arr, 10)
    print("线性查找1：元素在数组中的索引为 %d, 查找次数为 %d" % (result, counter))

def demo_22_sort() :
    data_list = [11, 13, 12, 5, 6]
    result, counter = sort_utils.insertion_sort(data_list)
    print("插入排序：插入排序结果为{},排序次数为{}".format(result, counter))
    print("快速排序：",sort_utils.quick_sort(data_list))
    print("选择排序：",sort_utils.selection_sort(data_list))
    print("冒泡排序：",sort_utils.bubble_sort(data_list))


if __name__ == '__main__':
    #print(demo_01_sum(1,2))
    #demo_02_sqrt_root(12)
    #demo_03_triangle_area(3,4,5)
    #demo_04_circle_area(5)
    #demo_05_prime(2, 100)
    #demo_06_numeric()
    #demo_07_multip_table()
    #demo_08_narcissistic_number()
    #demo_21_search_binary()
    demo_22_sort()
