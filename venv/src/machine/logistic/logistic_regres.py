
import numpy as np
import matplotlib.pyplot as plt
import random


def plot_logistic(data_mat, label_mat) :
    data_arr = np.array(data_mat)
    n = np.shape(data_mat)[0]
    xcord1 = []
    ycord1 = []  # 正样本
    xcord2 = []
    ycord2 = []  # 负样本
    for i in range(n):  # 根据数据集标签进行分类
        if int(label_mat[i]) == 1:
            xcord1.append(data_arr[i, 1]);
            ycord1.append(data_arr[i, 2])  # 1为正样本
        else:
            xcord2.append(data_arr[i, 1]);
            ycord2.append(data_arr[i, 2])  # 0为负样本
    fig = plt.figure()
    ax = fig.add_subplot(111)  # 添加subplot
    ax.scatter(xcord1, ycord1, s=20, c='red', marker='s', alpha=.5)  # 绘制正样本
    ax.scatter(xcord2, ycord2, s=20, c='green', alpha=.5)  # 绘制负样本
    plt.title('DataSet')  # 绘制title
    plt.xlabel('x');
    plt.ylabel('y')  # 绘制label
    plt.show()  # 显示


#def sigmoid(inX) :
#    return 1.0 / (1 + np.exp(-inX))

def sigmoid(inx):
    if inx>=0:      #对sigmoid函数的优化，避免了出现极大的数据溢出
        return 1.0/(1 + np.exp(-inx))
    else:
        return np.exp(inx) / (1 + np.exp(inx))

"""
gradient ascent 
梯度上升算法

"""
def grad_ascent(data_mat, labels) :
    # getA()函数与mat()函数的功能相反，是将一个numpy矩阵转换为数组
    data_matrix  = np.mat(data_mat)
    # 向量转置，transpose
    label_matrix = np.mat(labels).transpose()
    # m 表示矩阵的维度，n 表示矩阵的列；返回矩阵大小，m为行,n为列数(也是特征数)
    m,n = np.shape(data_matrix)
    alpha = 0.001
    max_cycle = 500
    weights = np.ones((n,1))
    for k in range(max_cycle) :
        h = sigmoid(data_matrix * weights)
        error = (label_matrix - h)
        # 将样本数据转置之后才可以做矩阵运算
        weights = weights + alpha * data_matrix.transpose() * error
    return weights.getA()

def grad_ascent_1(data_mat, labels) :
    # getA()函数与mat()函数的功能相反，是将一个numpy矩阵转换为数组
    data_matrix  = np.mat(data_mat)
    # 向量转置，transpose
    label_matrix = np.mat(labels).transpose()
    # m 表示矩阵的维度，n 表示矩阵的列；返回矩阵大小，m为行,n为列数(也是特征数)
    m,n = np.shape(data_matrix)
    alpha = 0.001
    max_cycle = 500
    weights = np.ones((n,1))
    weights_array = np.array([])
    for k in range(max_cycle) :
        h = sigmoid(data_matrix * weights)
        error = (label_matrix - h)
        # 将样本数据转置之后才可以做矩阵运算
        weights = weights + alpha * data_matrix.transpose() * error
        weights_array = np.append(weights_array, weights)
    weights_array = weights_array.reshape(max_cycle, n)
    return weights.getA(), weights_array

"""
此方法需要大量数据计算，
"""
def plot_best_fit(data_mat, label_mat,weights) :
    data_arr = np.array(data_mat)
    n = np.shape(data_mat)[0]
    xcord1 = []
    ycord1 = []  # 正样本
    xcord2 = []
    ycord2 = []  # 负样本
    for i in range(n):  # 根据数据集标签进行分类
        if int(label_mat[i]) == 1:
            xcord1.append(data_arr[i, 1]);
            ycord1.append(data_arr[i, 2])  # 1为正样本
        else:
            xcord2.append(data_arr[i, 1]);
            ycord2.append(data_arr[i, 2])  # 0为负样本
    fig = plt.figure()
    ax = fig.add_subplot(111)  # 添加subplot
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')  # 绘制正样本
    ax.scatter(xcord2, ycord2, s=30, c='green')  # 绘制负样本
    x = np.arange(-3.0, 3.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]
    ax.plot(x,y)
    plt.title('DataSet')  # 绘制title
    plt.xlabel('x');
    plt.ylabel('y')  # 绘制label
    plt.show()  # 显示


"""
gradient ascent 
"""
def stoc_grad_ascent_0(data_mat, labels) :
    data_mat = np.array(data_mat)
    # m 表示矩阵的维度，n 表示矩阵的列；返回矩阵大小，m为行,n为列数(也是特征数)
    m,n = np.shape(data_mat)
    alpha = 0.01
    weights = np.ones(n)
    for i in range(m) :
        h = sigmoid(sum(data_mat[i] * weights))
        error = labels[i] - h
        # 将样本数据转置之后才可以做矩阵运算
        weights = weights + alpha * error * data_mat[i]
    return weights



"""
gradient ascent:改进的随机梯度上升算法 
"""
def stoc_grad_ascent_1(data_mat, class_labels, num_iter = 150) :
    data_mat = np.array(data_mat)
    # m 表示矩阵的维度，n 表示矩阵的列；返回矩阵大小，m为行,n为列数(也是特征数)
    m,n = np.shape(data_mat)
    weights_array = np.array([])  # 存储每次更新的回归系数
    weights = np.ones(n)
    for j in range(num_iter) :
        data_index = list(range(m))
        for i in range(m):
            alpha = 4 / (1.0 + j + i) + 0.01  # 降低alpha的大小，每次减小1/(j+i)。
            rand_index = int(random.uniform(0, len(data_index)))  # 随机选取样本
            h = sigmoid(sum(data_mat[rand_index] * weights))  # 选择随机选取的一个样本，计算h
            error = class_labels[rand_index] - h  # 计算误差
            weights = weights + alpha * error * data_mat[rand_index]  # 更新回归系数
            weights_array = np.append(weights_array, weights, axis=0)  # 添加回归系数到数组中
            del (data_index[rand_index])  # 删除已经使用的样本
    weights_array = weights_array.reshape(num_iter * m, n)  # 改变维度
    return weights, weights_array  # 返回

def stoc_grad_ascent_2(data_mat, class_labels, num_iter = 150) :
    data_mat = np.array(data_mat)
    # m 表示矩阵的维度，n 表示矩阵的列；返回矩阵大小，m为行,n为列数(也是特征数)
    m,n = np.shape(data_mat)
    weights = np.ones(n)
    for j in range(num_iter) :
        data_index = list(range(m))
        for i in range(m):
            alpha = 4 / (1.0 + j + i) + 0.01  # 降低alpha的大小，每次减小1/(j+i)。
            rand_index = int(random.uniform(0, len(data_index)))  # 随机选取样本
            h = sigmoid(sum(data_mat[rand_index] * weights))  # 选择随机选取的一个样本，计算h
            error = class_labels[rand_index] - h  # 计算误差
            weights = weights + alpha * error * data_mat[rand_index]  # 更新回归系数
            del (data_index[rand_index])  # 删除已经使用的样本
    return weights  # 返回

"""
绘制回归系数与迭代次数的关系
"""
def plot_weights(weights_array1,weights_array2):
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签 
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    #设置汉字格式
    # font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
    #将fig画布分隔成1行1列,不共享x轴和y轴,fig画布的大小为(13,8)
    #当nrow=3,nclos=2时,代表fig画布被分为六个区域,axs[0][0]表示第一行第一列
    fig, axs = plt.subplots(nrows=3, ncols=2,sharex=False, sharey=False, figsize=(20,10))
    x1 = np.arange(0, len(weights_array1), 1)
    #绘制w0与迭代次数的关系
    axs[0][0].plot(x1,weights_array1[:,0])
    axs0_title_text = axs[0][0].set_title(u'梯度上升算法：回归系数与迭代次数关系')
    axs0_ylabel_text = axs[0][0].set_ylabel(u'W0')
    plt.setp(axs0_title_text, size=20, weight='bold', color='black')
    plt.setp(axs0_ylabel_text, size=20, weight='bold', color='black')
    #绘制w1与迭代次数的关系
    axs[1][0].plot(x1,weights_array1[:,1])
    axs1_ylabel_text = axs[1][0].set_ylabel(u'W1')
    plt.setp(axs1_ylabel_text, size=20, weight='bold', color='black')
    #绘制w2与迭代次数的关系
    axs[2][0].plot(x1,weights_array1[:,2])
    axs2_xlabel_text = axs[2][0].set_xlabel(u'迭代次数')
    axs2_ylabel_text = axs[2][0].set_ylabel(u'W1')
    plt.setp(axs2_xlabel_text, size=20, weight='bold', color='black')
    plt.setp(axs2_ylabel_text, size=20, weight='bold', color='black')

    x2 = np.arange(0, len(weights_array2), 1)
    #绘制w0与迭代次数的关系
    axs[0][1].plot(x2,weights_array2[:,0])
    axs0_title_text = axs[0][1].set_title(u'改进的随机梯度上升算法：回归系数与迭代次数关系')
    axs0_ylabel_text = axs[0][1].set_ylabel(u'W0')
    plt.setp(axs0_title_text, size=20, weight='bold', color='black')
    plt.setp(axs0_ylabel_text, size=20, weight='bold', color='black')
    #绘制w1与迭代次数的关系
    axs[1][1].plot(x2,weights_array2[:,1])
    axs1_ylabel_text = axs[1][1].set_ylabel(u'W1')
    plt.setp(axs1_ylabel_text, size=20, weight='bold', color='black')
    #绘制w2与迭代次数的关系
    axs[2][1].plot(x2,weights_array2[:,2])
    axs2_xlabel_text = axs[2][1].set_xlabel(u'迭代次数')
    axs2_ylabel_text = axs[2][1].set_ylabel(u'W1')
    plt.setp(axs2_xlabel_text, size=20, weight='bold', color='black')
    plt.setp(axs2_ylabel_text, size=20, weight='bold', color='black')

    plt.show()


