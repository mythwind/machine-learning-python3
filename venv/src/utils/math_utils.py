#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @author : mythwind 
# contact : 774202013@qq.com
# @datetime : 2020/3/9 10:02 上午 
# @File : math_utils.py
# @desc :
import numpy as np


def replace_nan_with_mean(data_mat):
    """
    将NaN替换成平均值，首先是剔除所有NaN值，计算平均值，再讲NaN替换成平均值
    :param data_mat:
    :return:
    """
    # 获取特征维度
    num_feat = np.shape(data_mat)[1]
    # 遍历数据集每一个维度
    for i in range(num_feat):
        # 利用该维度所有非NaN特征求取均值
        mean_vals = np.mean(data_mat[np.nonzero(~np.isnan(data_mat[:, i].A))[0], i])
        # 将该维度中所有NaN特征全部用均值替换
        data_mat[np.nonzero(np.isnan(data_mat[:, i].A))[0], i] = mean_vals
    return data_mat
