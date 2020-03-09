#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @author : mythwind 
# contact : 774202013@qq.com
# @datetime : 2020/3/3 2:56 下午 
# @File : mkmean.py
# @desc :

import numpy as np
import matplotlib.pyplot as plt
import math


def plot_xycord(xcord, ycord):
    fig = plt.figure()
    ax = fig.add_subplot(111)  # 添加subplot
    ax.scatter(xcord, ycord, s=20, c='blue', alpha=.5)  # 绘制样本点
    plt.title('dataset')  # 绘制title
    plt.xlabel('X')
    plt.show()


def plot_orginal_dataset(data_mat):
    n = len(data_mat)  # 数据个数
    # print(data_mat)
    xcord = []
    ycord = []  # 样本点
    for i in range(n):
        xcord.append(data_mat[i][0]);
        ycord.append(data_mat[i][1])  # 样本点
    plot_xycord(xcord, ycord)


def distance_eclud(veca, vecb):
    """
    距离计算公式(欧式距离)：多维平面距离计算公式
    :param veca:
    :param vecb:
    :return:
    """
    if type(veca).__name__ == 'list' :
        veca = np.mat(veca)
    if type(vecb).__name__ == 'list' :
        vecb = np.mat(vecb)
    return np.sqrt(np.sum(np.power(veca - vecb, 2)))


def random_center(dataset, k):
    """
    为数据集构建一个包含 k 个随机质心的集合
    :param dataset:
    :param k:
    :return:
    """
    n = np.shape(dataset)[1]
    # 如果是 list 而非 matrix，则转化一下
    if type(dataset).__name__ == 'list' :
        dataset = np.mat(dataset)
    centroids = np.mat(np.zeros((k, n)))
    for j in range(n):
        minj = min(dataset[:, j])
        rangej = float(max(dataset[:, j]) - minj)
        centroids[:, j] = minj + rangej * np.random.rand(k, 1)
    return centroids


def kmeans(dataset, k, dis_means = distance_eclud, create_cnter = random_center) :
    """
    K-均值聚类算法
    :param dataset:
    :param k: 簇的数目（簇的数目如何确定？）
    :param dis_means:
    :param create_cnter:
    :return:
    """
    # 如果是 list 而非 matrix，则转化一下
    if type(dataset).__name__ == 'list' :
        dataset = np.mat(dataset)
    m = np.shape(dataset)[0]
    # 簇分配结果矩阵：第一列存放索引
    cluster_assment = np.mat(np.zeros((m, 2)))
    centroids = create_cnter(dataset, k)
    cluster_changed = True
    while cluster_changed :
        cluster_changed = False
        for i in range(m) :
            min_distance = np.inf
            min_index = -1
            for j in range(k) :
                # 寻找最近的质心，计算数据集里面的每个点到质心的距离
                dist_JI = dis_means(centroids[j, :], dataset[i, :])
                if dist_JI < min_distance :
                    min_distance = dist_JI
                    min_index = j
            if cluster_assment[i, 0] != min_index :
                cluster_changed = True
            cluster_assment[i, :] = min_index, min_distance ** 2
        # print("kmeans.centroids： ", centroids)
        # 遍历所有的质心并更新他们的值
        for cent in range(k) :
            pts_clust = dataset[np.nonzero(cluster_assment[:, 0].A == cent)[0]]
            if len(pts_clust) != 0 :
                centroids[cent, :] = np.mean(pts_clust, axis=0)
    return centroids, cluster_assment


def binary_kmeans(dataset, k, dist_means = distance_eclud) :
    """
    二分K-Means算法
    两种方法：(1)是否可以最大程度的降低SSE的值   (2)选择SSE最大的簇进行划分
    :param dataset:
    :param k:
    :param dist_means:
    :return:
    """
    # 如果是 list 而非 matrix，则转化一下
    if type(dataset).__name__ == 'list':
        dataset = np.mat(dataset)
    m = np.shape(dataset)[0]
    # 簇分配结果矩阵：第一列存放索引
    cluster_assment = np.mat(np.zeros((m, 2)))
    # x = [[1,2,3],[4,5,6],[7,8,9]]
    # axis=0，那么输出矩阵是1行，求每一列的平均，一行取第一个元素
    # axis=1，输出矩阵是1列，求每一行的平均
    # centroid0 首先将整个数据集划分一个最大的簇
    centroid0 = np.mean(dataset, axis=0).tolist()[0]
    cent_list = [centroid0]
    for j in range(m) :
        # 计算数据集每个点到簇到距离
        cluster_assment[j, 1] = dist_means(np.mat(centroid0), dataset[j,:]) ** 2
    while len(cent_list) < k :
        # np.inf表示一个足够大的数
        lowest_sse = np.inf
        for i in range(len(cent_list)) :
            # 划分簇； 先取cluster_assment的第一列，cluster_assment[:,0].A == i 得到bool矩阵，然后分离0和非0索引
            pts_curr_cluster = dataset[np.nonzero(cluster_assment[:,0].A == i)[0], :]
            centroid_mat, split_asst = kmeans(pts_curr_cluster, 2, dist_means)
            # 计算误差值 split_asst
            sse_split = sum(split_asst[:,1])
            # 剩余数据集的误差值 sse_nosplit
            sse_nosplit = sum(cluster_assment[np.nonzero(cluster_assment[:, 0].A != i)[0], 1])
            print("sse_split and sse_nosplit : ", sse_split, sse_nosplit, i)
            if (sse_split + sse_nosplit) < lowest_sse :
                best_cent_split = i
                best_cents = centroid_mat
                best_cluster_asst = split_asst.copy()
                lowest_sse = sse_split + sse_nosplit
        # 更新簇结果
        best_cluster_asst[np.nonzero(best_cluster_asst[:, 0].A == 1)[0], 0] = len(cent_list)
        best_cluster_asst[np.nonzero(best_cluster_asst[:, 0].A == 0)[0], 0] = best_cent_split
        print("the best_cent_split is：", best_cent_split)
        print("the len of best_cluster_asst is：", len(best_cluster_asst))
        # 新的簇加入 cent_list
        cent_list[best_cent_split] = best_cents[0, :]
        cent_list.append(best_cents[1, :])
        # 更新SSE的值(sum of squared errors)
        cluster_assment[np.nonzero(cluster_assment[:, 0].A == best_cent_split)[0], :] = best_cluster_asst
    # 生成标准list
    cent_list = list(map(lambda x: [int(x[0]), x[1]], [np.matrix.tolist(i)[0] for i in cent_list]))
    return np.mat(cent_list), cluster_assment



def plot_kmeans(dataMat,centroids,clusterAssment):
    k=len(centroids)
    fig = plt.figure()
    dataMat = np.mat(dataMat)
    ax = fig.add_subplot(111)
    ax.scatter(centroids[:,0].tolist(),centroids[:,1].tolist(),marker='+',c='r')
    markers=['o','s','v','*'];
    clrs=['blue','green','yellow','red']
    for i in range(k):
        data_class = dataMat[np.nonzero(clusterAssment[:,0].A == i)[0]]
        ax.scatter(data_class[:,0].tolist(),data_class[:,1].tolist(),marker=markers[i],c=clrs[i])
    plt.show()



def dist_slc(vecta, vectb) :
    """
    球面距离计算公式：AREA = R·arc cos[cosβ1cosβ2cos（α1-α2）+ sinβ1sinβ2]
    :param vecta:
    :param vectb:
    :return:
    """
    a = np.sin(vecta[0, 1] * math.pi / 180) * np.sin(vectb[0, 1] * math.pi / 180)
    b = np.cos(vecta[0, 1] * math.pi / 180) * np.cos(vectb[0, 1] * math.pi / 180) * np.cos(math.pi * (vectb[0, 0] - vecta[0, 0]) / 180)
    #  6371 地球近似半径
    return np.arccos(a + b) * 6371.0


def cluster_clubs(data_mat, num_cluster = 5) :
    """
    对地理坐标聚集，绘制出坐标图
    :param data_mat:
    :param num_cluster:
    :return:
    """
    # 如果是 list 而非 matrix，则转化一下
    if type(data_mat).__name__ == 'list':
        data_mat = np.mat(data_mat)
    cent_list, cluster_assment = binary_kmeans(data_mat, num_cluster, dist_means=dist_slc)

    fig = plt.figure()
    plt.subplot(111)
    rect = [0.1, 0.1, 0.8, 0.8]
    markers = ['s', 'o', '^', '8', 'p', 'd', 'v', 'h', '>', '<']
    axprops = dict(xticks=[], yticks=[])
    ax0 = fig.add_axes(rect, label='ax0', **axprops)
    imgp = plt.imread('assets/Portland.png')
    ax0.imshow(imgp)
    ax1 = fig.add_axes(rect, label='ax1', frameon = False)
    for i in range(num_cluster) :
        pts_curr_cluster = data_mat[np.nonzero(cluster_assment[:, 0].A == i)[0], :]
        marker_style = markers[i % len(markers)]
        ax1.scatter(pts_curr_cluster[:, 0].flatten().A[0], pts_curr_cluster[:, 1].flatten().A[0], marker=marker_style, s=90)
    ax1.scatter(cent_list[:, 0].flatten().A[0], cent_list[:, 1].flatten().A[0], marker='+', s=90, c='r')
    ## UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect. warnings.warn("This figure includes Axes that are not compatible "
    plt.savefig('fig.png', bbox_inches='tight')  # 替换 plt.show()
    # plt.show()




