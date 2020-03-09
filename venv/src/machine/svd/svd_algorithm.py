#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @author : mythwind 
# contact : 774202013@qq.com
# @datetime : 2020/3/9 10:24 上午 
# @File : svd_algorithm.py
# @desc :
import numpy as np
from numpy import linalg as la


def euclid_similar(col_vector_a, col_vector_b):
    """
    欧几里得范数
    :param col_vector_a: 列向量
    :param col_vector_b:
    :return:
    """
    # 其中的axis=0表示对矩阵的每一列求范数，axis=1表示对矩阵的每一行求范数， keeptime=True表示结果保留二维特性，keeptime=False表示结果不保留二维特性
    return 1.0 / (1.0 + la.norm(col_vector_a - col_vector_b))


def pearson_similar(col_vector_a, col_vector_b):
    """
    皮尔逊积矩相关系数
    :param col_vector_a:
    :param col_vector_b:
    :return:
    """
    # 检查是否存在三个或更多的点，若不存在，则返回1.0，这是因为此时两个向量完全相关
    if len(col_vector_a) < 3: return 1.0
    return 0.5 + 0.5 * np.corrcoef(col_vector_a, col_vector_b, rowvar=0)[0][1]


def cosine_similar(col_vector_a, col_vector_b):
    """
    余弦相似度用向量空间中两个向量夹角的余弦值作为衡量两个个体间差异的大小。余弦值越接近1，就表明夹角越接近0度，也就是两个向量越相似，这就叫"余弦相似性"。
    :param col_vector_a:
    :param col_vector_b:
    :return:
    """
    num = float(col_vector_a.T * col_vector_b)
    denom = la.norm(col_vector_a) * la.norm(col_vector_b)
    return 0.5 + 0.5 * (num / denom)



def stand_estimated(data_mat, user, sim_meas, item):
    """
    评分系统：用来计算在给定相似度计算方法的条件下，用户对物品的估计评分值
    :param data_mat:
    :param user:
    :param sim_meas:
    :param item:
    :return:
    """
    # 首先得到数据集中的物品数目
    n = np.shape(data_mat)[1]
    # 对两个用于计算估计评分值的变量进行初始化
    similar_total = 0.0
    rat_similar_total = 0.0
    for j in range(n):
        user_rating = data_mat[user, j]
        # 如果某个物品评分值为0，意味着用户没有对该物品评分，跳过
        if user_rating == 0 :
            continue
        # 寻找两个用户都评级的物品，变量overlap给出的是两个物品当中已经被评分的那个元素
        overlap = np.nonzero(np.logical_and(data_mat[:, item].A > 0, data_mat[:, j].A > 0))[0]
        # 若两者没有任何重合元素，则相似度为0且中止本次循环
        if len(overlap) == 0:
            similarity = 0
        else :
            # 如果存在重合的物品，则基于这些重合物品计算相似度
            similarity = sim_meas(data_mat[overlap, item], data_mat[overlap, j])
        # print("the {} and {} similarity is : {}".format(item, j, similarity))
        # 随后相似度不断累加
        similar_total += similarity
        rat_similar_total += similarity * user_rating
    if similar_total == 0:
        return 0
    else :
        # 通过除以所有的评分总和，对上述相似度评分的乘积进行归一化。这使得评分值在0-5之间，
        # 而这些评分值则用于对预测值进行排序
        return rat_similar_total / similar_total


def recommend_engine(data_mat, user, N=3, sim_meas=cosine_similar, estimated_method=stand_estimated):
    """
    推荐引擎，会调用stand_estimated评分函数，产生最高的N个推荐结果。
    :param data_mat:
    :param user:
    :param N:   寻找前N个未评级物品
    :param sim_meas:    相似度计算方法
    :param estimated_method:    估计方法
    :return:
    """
    # 寻找未评级的物品，对给定用户建立一个未评分的物品列表
    unrated_items = np.nonzero(data_mat[user, :].A == 0)[1]
    # 如果不存在未评分物品，退出函数，否则在所有未评分物品上进行循环
    if len(unrated_items) == 0:
        return 'You are rated everything'
    item_scores = []
    for item in unrated_items:
        # 对于每个未评分物品，通过调用stand_estimated()来产生该物品的预测评分。
        estimated_score = estimated_method(data_mat, user, sim_meas, item)
        # 该物品的编号和估计得分值会放在一个元素列表 item_scores
        item_scores.append((item, estimated_score))
    return sorted(item_scores, key=lambda jj: jj[1], reverse=True)[:N]



def svd_estimated(data_mat, user, sim_meas, item):
    # 首先得到数据集中的物品数目
    n = np.shape(data_mat)[1]
    # 对两个用于计算估计评分值的变量进行初始化
    similar_total = 0.0
    rat_similar_total = 0.0
    U, sigma, vt = np.linalg.svd(np.mat(data_mat))
    # 取前4行奇异值
    # 使用奇异值构建一个对角矩阵
    sig4 = np.mat(np.eye(4) * sigma[:4])
    xformed_items = data_mat.T * U[:, :4] * sig4.I
    for j in range(n):
        user_rating = data_mat[user, j]
        # 若两者没有任何重合元素，则相似度为0且中止本次循环
        if user_rating == 0 or j == item:
            continue
        # 如果存在重合的物品，则基于这些重合物品计算相似度
        similarity = sim_meas(xformed_items[item, :].T, xformed_items[j, :].T)
        # print("the {} and {} similarity is : {}".format(item, j, similarity))
        # 随后相似度不断累加
        similar_total += similarity
        rat_similar_total += similarity * user_rating
    if similar_total == 0:
        return 0
    else:
        # 通过除以所有的评分总和，对上述相似度评分的乘积进行归一化。这使得评分值在0-5之间，
        # 而这些评分值则用于对预测值进行排序
        return rat_similar_total / similar_total


def print_mat(data_mat, thresh=0.8):
    for i in range(32):
        for k in range(32):
            if float(data_mat[i, k]) > thresh:
                print(1, end=' ')
            else :
                print(0, end=' ')
        print('')


def image_compress(data_mat, num_sv=3, thresh=0.8):
    print("******original matrix******")
    print_mat(data_mat, thresh)
    # 对原始图像进行SVD分解并重构图像，通过将Sigma重构成SigRecon来实现
    U, Sigma, VT = la.svd(data_mat)
    # Sigma是一个对角矩阵，需要建立一个全0矩阵，然后将前面的那些奇异值填充到对角线上。
    SigRecon = np.mat(np.zeros((num_sv, num_sv)))
    for k in range(num_sv):
        SigRecon[k, k] = Sigma[k]
    # 通过截断的U和VT矩阵，用SigRecon得到重构后的矩阵
    reconMat = U[:, :num_sv] * SigRecon * VT[:num_sv, :]
    print("******reconstructed matrix using %d singular values******" % num_sv)
    print_mat(reconMat, thresh)




