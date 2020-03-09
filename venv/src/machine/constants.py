
# -*- coding: utf-8 -*-]
# Filename:constants.py
# 定义一个常量类实现常量的功能
#
# 该类定义了一个方法__setattr()__,和一个异常ConstError, ConstError类继承
# 自类TypeError. 通过调用类自带的字典__dict__, 判断定义的常量是否包含在字典
# 中。如果字典中包含此变量，将抛出异常，否则，给新创建的常量赋值。
# 最后两行代码的作用是把const类注册到sys.modules这个全局字典中。

class constants:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

        # 重写 __setattr__() 方法
        def __setattr__(self, name, value):
            if name in self.__dict__:  # 已包含该常量，不能二次赋值
                raise self.ConstError("Can't change const {0}".format(name))
            if not name.isupper():  # 所有的字母需要大写
                raise self.ConstCaseError("const name {0} is not all uppercase".format(name))
            self.__dict__[name] = value

import sys
sys.modules[__name__] = constants()


constants.PI = 3.14
constants.FILE_TREE_CLFS_PATH = 'assets/classifierStorage.txt'
constants.FILE_TREE_LENSES_PATH = 'assets/lenses.txt'
constants.DIR_BAYES_SPAN_PATH = 'assets/spam'
constants.DIR_BAYES_HAM_PATH = 'assets/ham'
constants.FILE_LOGISTIC_DATA_PATH = 'assets/testSet.txt'
constants.FILE_LOGISTIC_HORSE_TEST_PATH = 'assets/horseColicTest.txt'
constants.FILE_LOGISTIC_HORSE_TRAINING_PATH = 'assets/horseColicTraining.txt'
constants.FILE_SVM_DATA_PATH = 'assets/testSet.txt'
constants.FILE_ADABOOST_TEST_PATH = 'assets/horseColicTest2.txt'
constants.FILE_ADABOOST_TRAIN_PATH = 'assets/horseColicTraining2.txt'
constants.FILE_ADABOOST_TRAIN_PATH = 'assets/horseColicTraining2.txt'
constants.FILE_REGRESSION_0_PATH = 'assets/ex0.txt'
constants.FILE_REGRESSION_1_PATH = 'assets/ex1.txt'
constants.FILE_REGRESSION_ABALONE_PATH = 'assets/abalone.txt'
constants.FILE_TREE_EX00_PATH = 'assets/ex00.txt'
constants.FILE_TREE_EX0_PATH = 'assets/ex0.txt'
constants.FILE_TREE_EX2_PATH = 'assets/ex2.txt'
constants.FILE_TREE_EX2TEST_PATH = 'assets/ex2test.txt'
constants.FILE_TREE_EXP2_PATH = 'assets/exp2.txt'
constants.FILE_TREE_BIKE_TEST_PATH = 'assets/bikeSpeedVsIq_test.txt'
constants.FILE_TREE_BIKE_TRAIN_PATH = 'assets/bikeSpeedVsIq_train.txt'
constants.FILE_KMEAN_TEST1_PATH = 'assets/testSet.txt'
constants.FILE_KMEAN_TEST2_PATH = 'assets/testSet2.txt'

constants.FILE_FPGROUTH_DATA_PATH = 'assets/kosarak.dat'




