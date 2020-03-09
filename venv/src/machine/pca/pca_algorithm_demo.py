#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @author : mythwind 
# contact : 774202013@qq.com
# @datetime : 2020/3/9 9:30 上午 
# @File : pca_algorithm_demo.py
# @desc :
from utils import file_utils
from utils import math_utils
from pca import pca_algorithm
import numpy as np


def test_data():
    data_mat = file_utils.load_map_datamat("assets/testSet.txt")
    lowd_mat, recon_mat = pca_algorithm.pca_dimen_reduce(data_mat, 1)
    print(np.shape(data_mat))
    print(np.shape(lowd_mat))
    pca_algorithm.plot_datamat(data_mat, lowd_mat, recon_mat)

def test_secom() :
    data_mat = file_utils.load_map_datamat("assets/secom.data", ' ')
    data_mat = math_utils.replace_nan_with_mean(data_mat)
    pca_algorithm.show_secom_data(data_mat)


if __name__ == '__main__':
    test_data()
    test_secom()
