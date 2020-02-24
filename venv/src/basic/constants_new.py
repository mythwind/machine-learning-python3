
# -*- coding: utf-8 -*-]
# Filename:constants.py
# 定义一个常量类实现常量的功能
#
# 该类定义了一个方法__setattr()__,和一个异常ConstError, ConstError类继承
# 自类TypeError. 通过调用类自带的字典__dict__, 判断定义的常量是否包含在字典
# 中。如果字典中包含此变量，将抛出异常，否则，给新创建的常量赋值。
# 最后两行代码的作用是把const类注册到sys.modules这个全局字典中。

"""
另外一种定义常量的方法　
"""
class _mconstants(object) :
    def __init__(self):
        self.__PI = 3.1415926
        self.__FILE_PATH_FOO = "assets/foo.txt"
        self.__FILE_PATH_PKL = "assets/data.pkl"
        self.__FILE_XML_MOIVES = "assets/moives.xml"
        self.__FILE_JSON_DATA = "assets/data.json"

    @property
    def PI(self):
        return self.__PI

    @property
    def FILE_PATH_FOO(self):
        return self.__FILE_PATH_FOO

    @property
    def FILE_PATH_PKL(self):
        return self.__FILE_PATH_PKL

    @property
    def FILE_XML_MOIVES(self):
        return self.__FILE_XML_MOIVES

    @property
    def FILE_JSON_DATA(self):
        return self.__FILE_JSON_DATA

