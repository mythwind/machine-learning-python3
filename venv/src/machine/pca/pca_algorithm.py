#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @author : mythwind 
# contact : 774202013@qq.com
# @datetime : 2020/3/8 3:16 下午 
# @File : pca_algorithm.py
# @desc :
import numpy as np
import matplotlib.pyplot as plt
from utils import math_utils

def  plot_datamat(original_data, lowd_data, recon_mat):
    # 画图
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(lowd_data[:,0].flatten().A[0],np.zeros(len(lowd_data)))   # 降维后的图
    ax.scatter(original_data[:, 0].flatten().A[0], original_data[:, 1].flatten().A[0], marker='^', s=90)
    ax.scatter(recon_mat[:, 0].flatten().A[0], recon_mat[:, 1].flatten().A[0], marker='o', s=50, c='red')
    plt.show()


def pca_dimen_reduce(data_mat, topn_feat=9999999):
    """
    特征维度压缩函数，不指定压缩维数默认9999999即维数全部返回;
    减去均值后再除以标准差得出的数值就是标准化数据
    :param data_mat:
    :param topn_feat: 需要保留的特征维度，即要压缩成的维度数
    :return:
    """
    # 平均值
    mean_vals = np.mean(data_mat, axis=0)
    # 数据矩阵每一列减去该列的特征均值
    mean_removed = data_mat - mean_vals
    # 计算协方差矩阵，除数n-1是为了得到协方差的无偏估计
    covmat = np.cov(mean_removed, rowvar=0)
    # 计算矩阵的特征值个特征向量
    eig_vals, eig_vects = np.linalg.eig(np.mat(covmat))
    # sort():对特征值矩阵排序(由小到大)
    # argsort():对特征值矩阵进行由小到大排序，返回对应排序后的索引
    eig_val_ind = np.argsort(eig_vals)
    #从排序后的矩阵最后一个开始自下而上选取最大的N个特征值，返回其对应的索引
    eig_val_ind = eig_val_ind[: -(topn_feat + 1): -1]
    #将特征值最大的N个特征值对应索引的特征向量提取出来，组成压缩矩阵
    reduce_eig_vects = eig_vects[:, eig_val_ind]
    # 将去除均值后的数据矩阵*压缩矩阵，转换到新的空间，使维度降低为N
    low_dimen_data = mean_removed * reduce_eig_vects
    # 利用降维后的矩阵反构出原数据矩阵(用作测试，可跟未压缩的原矩阵比对)
    reco_mat = (low_dimen_data * reduce_eig_vects.T) + mean_vals
    return low_dimen_data, reco_mat


def show_secom_data(data_mat):
    data_mat = math_utils.replace_nan_with_mean(data_mat)
    meanVals = np.mean(data_mat, axis=0)
    meanRemoved = data_mat - meanVals
    covMat = np.cov(meanRemoved, rowvar=0)
    eigVals, eigVects = np.linalg.eig(np.mat(covMat))
    print(eigVals)
    print(sum(eigVals) * 0.9)  # 计算90%的主成分方差总和
    print(sum(eigVals[:6]))  # 计算前6个主成分所占的方差
    plt.plot(eigVals[:20])  # 对前20个画图观察
    plt.show()

