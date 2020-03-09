# -*- coding:UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import random
import os

"""
数组转置（T）
轴对换之transpose
两轴对换swapaxes
"""

def load_data_from_file(filename) :
    data_mat = []
    label_mat = []
    fr = open(filename)
    for line in fr.readlines():  # 逐行读取，滤除空格等
        line_arr = line.strip().split('\t')
        data_mat.append([float(line_arr[0]),float(line_arr[1])])
        label_mat.append(float(line_arr[2]))
    return data_mat, label_mat

"""
随机选择alpha
    i - alpha
    m - alpha参数个数
"""
def select_jrand(i,m) :
    j = i
    # 选择一个不等于i的j
    while(j == i) :
        j = int(random.uniform(0,m))
    return j

"""
设置alpha上下限
"""
def clip_alpha(aj,high,low) :
    if aj > high :
        aj = high
    if aj < low :
        aj = low
    return aj

"""
简化版SMO算法
数据集，标签集，常数C，容错率，退出前最大循环次数
"""
def smo_simple(data_mat_in,class_labels,C,toler,max_iter) :
    # 转换为numpy的mat存储
    data_matrix = np.mat(data_mat_in)
    label_mat = np.mat(class_labels).transpose()
    # 初始化b参数，统计dataMatrix的维度
    b = 0
    m, n = np.shape(data_matrix)
    # 初始化alpha参数，设为0
    alphas = np.mat(np.zeros((m, 1)))
    # 初始化迭代次数
    iter_num = 0
    # 最多迭代matIter次
    while (iter_num < max_iter) :
        alpha_pairs_changed = 0
        for i in range(m) :
            # 步骤1：计算误差Ei
            fxi = float(np.multiply(alphas, label_mat).T * (data_matrix * data_matrix[i, :].T)) + b
            Ei = fxi - float(label_mat[i])
            # 优化alpha，更设定一定的容错率。
            if ((label_mat[i] * Ei < -toler) and (alphas[i] < C)) or ((label_mat[i] * Ei > toler) and (alphas[i] > 0)) :
                # 随机选择另一个与alpha_i成对优化的alpha_j
                j = select_jrand(i,m)
                # 计算误差Ej
                fxj = float(np.multiply(alphas, label_mat).T * (data_matrix * data_matrix[j, :].T)) + b
                Ej = fxj - float(label_mat[j])
                # 保存更新前的aplpha值，使用深拷贝
                alpha_i_old = alphas[i].copy()
                alpha_j_old = alphas[j].copy()
                # 计算上下界
                if label_mat[i] != label_mat[j] :
                    H = max(0, alphas[j] - alphas[i])
                    L = min(C, C + alphas[j] - alphas[i])
                else:
                    H = max(0, alphas[j] + alphas[i] - C)
                    L = min(C, alphas[j] + alphas[i])
                if L == H:
                    #print("L==H");
                    continue
                # 步骤3：计算eta
                eta = 2.0 * data_matrix[i,:] * data_matrix[j,:].T - data_matrix[i,:] * data_matrix[i,:].T - data_matrix[j,:] * data_matrix[j,:].T
                if eta >= 0:
                    #print("eta>=0");
                    continue
                # 步骤4：更新alpha_j
                alphas[j] -= label_mat[j] * (Ei - Ej) / eta
                # 步骤5：修剪alpha_j
                alphas[j] = clip_alpha(alphas[j], H, L)
                if (abs(alphas[j] - alpha_j_old) < 0.00001):
                    # print("alpha_j变化太小");
                    continue
                # 步骤6：更新alpha_i
                alphas[i] += label_mat[j] * label_mat[i] * (alpha_j_old - alphas[j])
                # 步骤7：更新b_1和b_2
                b1 = b - Ei - label_mat[i] * (alphas[i] - alpha_i_old) * data_matrix[i, :] * data_matrix[i, :].T - label_mat[j] * (alphas[j] - alpha_j_old) * data_matrix[i, :] * data_matrix[j, :].T
                b2 = b - Ej - label_mat[i] * (alphas[i] - alpha_i_old) * data_matrix[i, :] * data_matrix[j, :].T - label_mat[j] * (alphas[j] - alpha_j_old) * data_matrix[j, :] * data_matrix[j, :].T
                # 步骤8：根据b_1和b_2更新b
                if (0 < alphas[i]) and (C > alphas[i]):
                    b = b1
                elif (0 < alphas[j]) and (C > alphas[j]):
                    b = b2
                else:
                    b = (b1 + b2) / 2.0
                # 统计优化次数
                alpha_pairs_changed += 1
                # 打印统计信息
                print("第%d次迭代 样本:%d, alpha优化次数:%d" % (iter_num, i, alpha_pairs_changed))
        # 更新迭代次数
        if (alpha_pairs_changed == 0):
            iter_num += 1
        else:
            iter_num = 0
        print("迭代次数: %d" % iter_num)
    return b, alphas

def calc_ws(data_mat,label_mat,alphas) :
     # list不能使用reshape，需要将其转化为array，然后就可以使用reshape了
    return np.dot((np.tile(np.array(label_mat).reshape(1, -1).T, (1, 2)) * data_mat).T, alphas)

def show_classifer(data_mat,label_mat,alphas,w,b) :
    # 绘制样本点
    data_plus = []  # 正样本
    data_minus = []  # 负样本
    for i in range(len(data_mat)):
        if label_mat[i] > 0:
            data_plus.append(data_mat[i])
        else:
            data_minus.append(data_mat[i])
    data_plus_np = np.array(data_plus)  # 转换为numpy矩阵
    data_minus_np = np.array(data_minus)  # 转换为numpy矩阵
    plt.scatter(np.transpose(data_plus_np)[0], np.transpose(data_plus_np)[1], s=30, alpha=0.7)  # 正样本散点图
    plt.scatter(np.transpose(data_minus_np)[0], np.transpose(data_minus_np)[1], s=30, alpha=0.7)  # 负样本散点图
    # 绘制直线
    x1 = max(data_mat)[0]
    x2 = min(data_mat)[0]
    a1, a2 = w
    b = float(b)
    a1 = float(a1[0])
    a2 = float(a2[0])
    y1, y2 = (-b- a1*x1)/a2, (-b - a1*x2)/a2
    plt.plot([x1, x2], [y1, y2])
    #找出支持向量点
    for i, alpha in enumerate(alphas):
        if abs(alpha) > 0:
            x, y = data_mat[i]
            plt.scatter([x], [y], s=150, c='none', alpha=0.7, linewidth=1.5, edgecolor='red')
    plt.show()




