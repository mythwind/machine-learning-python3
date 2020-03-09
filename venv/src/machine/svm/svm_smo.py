# -*- coding:UTF-8 -*-
import numpy as np
import random

class OptStruct :
    def __init__(self, data_mat, class_labels, C, toler):
        self.X = data_mat
        self.label_mat = class_labels
        self.C = C
        self.toler = toler
        self.m = np.shape(data_mat)[0]
        self.alphas = np.mat(np.zeros((self.m,1)))
        self.b = 0
        # 根据矩阵行数初始化误差缓存，第一列为是否有效的标志位，第二列为实际的误差E的值。
        self.ecache = np.mat(np.zeros((self.m,2)))

    def __str__(self,print_all=False):  # 定义打印对象时打印的字符串
        if print_all:
            return '***'.join(('%s' % item for item in self.__dict__.values()))
        else:
            return self.label_mat

    def is_alpha_optimable(self, i, Ei):
        return ((self.label_mat[i] * Ei < -self.toler) and (self.alphas[i] < self.C)) or ((self.label_mat[i] * Ei > self.toler) and (self.alphas[i] > 0))

    def alpha_add(self, i, j):
        return self.alphas[i] + self.alphas[j]

    def alpha_subtract(self, j, i):
        return self.alphas[j] - self.alphas[i]

    def get_eta (self,i,j):
        # 矩阵的第 i 行乘以矩阵的第 j 行
        return 2.0 * self.X[i,:] * self.X[j,:].T - self.X[i,:] * self.X[i,:].T - self.X[j,:] * self.X[j,:].T

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
计算误差
"""
def calc_Ek(opt_struct,k) :
    fxk = float(np.multiply(opt_struct.alphas, opt_struct.label_mat).T * (opt_struct.X * opt_struct.X[k, :].T)) + opt_struct.b
    Ek = fxk - float(opt_struct.label_mat[k])
    return Ek

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
内循环中启发式方法

"""
def select_j(i, opt_struct, Ei) :
    max_k = -1
    max_delta_e = 0
    Ej = 0
    # 根据Ei更新误差缓存
    opt_struct.ecache[i] = [1,Ei]
    # 返回误差不为0的数据的索引值
    valid_ecache_list = np.nonzero(opt_struct.ecache[:,0].A)[0]
    if len(valid_ecache_list) > 1 :
        for k in valid_ecache_list :
            if k == i : continue
            Ek = calc_Ek(opt_struct, k)
            # 计算|Ei-Ek|
            delta_e =  abs(Ei - Ek)
            if delta_e > max_delta_e :
                max_k = k
                max_delta_e = delta_e
                Ej = Ek
        return max_k, Ej
    else :
        j = select_jrand(i,opt_struct.m)
        Ej = calc_Ek(opt_struct,j)
    return j,Ej

"""
计算Ek,并更新误差缓存
"""
def update_Ek(opt_struct, k) :
    Ek = calc_Ek(opt_struct, k)
    opt_struct.ecache[k] = [1, Ek]



def innerL(i, opt_struct) :
    Ei = calc_Ek(opt_struct, i)
    if opt_struct.is_alpha_optimable(i,Ei) :
        j, Ej = select_j(i, opt_struct, Ei)
        # 保存更新前的aplpha值，使用深拷贝
        alpha_i_old = opt_struct.alphas[i].copy()
        alpha_j_old = opt_struct.alphas[j].copy()
        # 计算上下界
        if opt_struct.label_mat[i] != opt_struct.label_mat[j]:
            H = max(0, opt_struct.alpha_subtract(j,i))
            L = min(opt_struct.C, opt_struct.C + opt_struct.alpha_subtract(j,i))
        else:
            H = max(0, opt_struct.alpha_add(i,j) - opt_struct.C)
            L = min(opt_struct.C, opt_struct.alpha_add(i,j))
        if L == H :
            # print("L==H")
            return 0
        eta = opt_struct.get_eta(i,j)
        if eta >= 0 :
            # print("eta >= 0")
            return 0
        # 步骤4：更新alpha_j
        opt_struct.alphas[j] -= opt_struct.label_mat[j] * (Ei - Ej) / eta
        # 步骤5：修剪alpha_j
        opt_struct.alphas[j] = clip_alpha(opt_struct.alphas[j], H, L)
        update_Ek(opt_struct,j)
        if (abs(opt_struct.alphas[j] - alpha_j_old) < 0.00001):
            # print("j not moving enought!")
            return 0
        opt_struct.alphas[i] += opt_struct.label_mat[j] * opt_struct.label_mat[i] * (alpha_j_old - opt_struct.alphas[j])
        update_Ek(opt_struct,i)

        # 步骤7：更新b_1和b_2
        b1 = opt_struct.b - Ei \
             - opt_struct.label_mat[i] * (opt_struct.alphas[i] - alpha_i_old) * opt_struct.X[i, :] * opt_struct.X[i, :].T \
             - opt_struct.label_mat[j] * (opt_struct.alphas[j] - alpha_j_old) * opt_struct.X[i, :] * opt_struct.X[j, :].T
        b2 = opt_struct.b - Ej \
             - opt_struct.label_mat[i] * (opt_struct.alphas[i] - alpha_i_old) * opt_struct.X[i, :] * opt_struct.X[j, :].T \
             - opt_struct.label_mat[j] * (opt_struct.alphas[j] - alpha_j_old) * opt_struct.X[j, :] * opt_struct.X[j, :].T
        # 步骤8：根据b_1和b_2更新b
        if (0 < opt_struct.alphas[i]) and (opt_struct.C > opt_struct.alphas[i]):
            opt_struct.b = b1
        elif (0 < opt_struct.alphas[j]) and (opt_struct.C > opt_struct.alphas[j]):
            opt_struct.b = b2
        else:
            opt_struct.b = (b1 + b2) / 2.0
        return 1
    else:
        return 0

def smo_p(data_mat,class_labels,C,toler,max_iter,k_tup=('lin',0)) :
    opt_str = OptStruct(np.mat(data_mat),np.mat(class_labels).transpose(),C,toler)
    iter = 0
    entry_set = True
    alpha_pairs_changed = 0
    while (iter < max_iter) and ((alpha_pairs_changed > 0) or (entry_set)) :
        alpha_pairs_changed = 0
        if entry_set :
            for i in range(opt_str.m) :
                # 使用优化的SMO算法
                alpha_pairs_changed += innerL(i, opt_str)
                print("全样本遍历:第%d次迭代 样本:%d, alpha优化次数:%d" % (iter, i, alpha_pairs_changed))
            iter += 1
        else :
            # 遍历非边界值
            # 遍历不在边界0和C的alpha
            non_bounds = np.nonzero((opt_str.alphas.A > 0) * (opt_str.alphas.A < C))[0]
            for i in non_bounds:
                alpha_pairs_changed += innerL(i, opt_str)
                print("非边界遍历:第%d次迭代 样本:%d, alpha优化次数:%d" % (iter, i, alpha_pairs_changed))
            iter += 1
        if entry_set:  # 遍历一次后改为非边界遍历
            entry_set = False
        elif (alpha_pairs_changed == 0):  # 如果alpha没有更新,计算全样本遍历
            entry_set = True
        print("迭代次数: %d" % iter)
        return opt_str.b, opt_str.alphas  # 返回SMO算法计算的b和alphas

def calc_ws(data_arr, class_labels,alphas) :
    data_mat = np.mat(data_arr);
    label_mat = np.mat(class_labels).transpose()
    m, n = np.shape(data_mat)
    w = np.zeros((n, 1))
    for i in range(m):
        w += np.multiply(alphas[i] * label_mat[i], data_mat[i, :].T)
    return w
