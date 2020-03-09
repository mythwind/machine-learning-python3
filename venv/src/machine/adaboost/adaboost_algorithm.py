# -*-coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

"""
从文件读取数据
"""
def load_dataset_from_file(filename) :
    num_feat = len(open(filename).readline().split('\t'))
    data_mat = []
    label_mat = []
    fr = open(filename)
    for line in fr.readlines() :
        line_arr = []
        curr_line = line.strip().split('\t')
        for i in range(num_feat - 1) :
            line_arr.append(float(curr_line[i]))
        data_mat.append(line_arr)
        label_mat.append(float(curr_line[-1]))
    return data_mat, label_mat


"""
数据可视化
Parameters:
    dataMat - 数据矩阵
    labelMat - 数据标签
"""
def show_dataset(dataMat, labelMat):
    data_plus = []                                  #正样本
    data_minus = []                                 #负样本
    for i in range(len(dataMat)):
        if labelMat[i] > 0:
            data_plus.append(dataMat[i])
        else:
            data_minus.append(dataMat[i])
    data_plus_np = np.array(data_plus)                                             #转换为numpy矩阵
    data_minus_np = np.array(data_minus)                                         #转换为numpy矩阵
    plt.scatter(np.transpose(data_plus_np)[0], np.transpose(data_plus_np)[1])        #正样本散点图
    plt.scatter(np.transpose(data_minus_np)[0], np.transpose(data_minus_np)[1])     #负样本散点图
    plt.show()

"""
单层决策树分类函数
    
"""
def stump_classify(data_matrix,dimen,thresh_val,inequal) :
    result_arr = np.ones((np.shape(data_matrix)[0], 1))  # 初始化result_arr为1
    if inequal == 'lt':
        result_arr[data_matrix[:, dimen] <= thresh_val] = -1.0  # 如果小于阈值,则赋值为-1
    else:
        result_arr[data_matrix[:, dimen] > thresh_val] = -1.0  # 如果大于阈值,则赋值为-1
    return result_arr

"""
找到数据集上最佳的单层决策树
"""
def build_stump(data_arr, class_labels,D) :
    data_matrix = np.mat(data_arr)
    label_matrix = np.mat(class_labels).T
    m,n = np.shape(data_matrix)
    num_steps = 10.0
    best_stump = {}
    best_class_est = np.mat(np.zeros((m,1)))
    min_error = float('inf')
    for i in range(n) :
        range_min = data_matrix[:,i].min()
        range_max = data_matrix[:,i].max()
        step_size = (range_max - range_min) / num_steps
        for j in range(-1, int(num_steps) + 1) :
            for inequal in ('lt','gt') :
                thresh_val = (range_min + float(j) * step_size)
                predicted_vals = stump_classify(data_matrix, i, thresh_val, inequal)#计算分类结果
                err_arr = np.mat(np.ones((m, 1)))  # 初始化误差矩阵
                err_arr[predicted_vals == label_matrix] = 0  # 分类正确的,赋值为0
                weighted_error = D.T * err_arr  # 计算误差
                # print("split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" % (i, thresh_val, inequal, weighted_error))
                if weighted_error < min_error:  # 找到误差最小的分类方式
                    min_error = weighted_error
                    best_class_est = predicted_vals.copy()
                    best_stump['dim'] = i
                    best_stump['thresh'] = thresh_val
                    best_stump['ineq'] = inequal
    return best_stump, min_error, best_class_est

"""
使用AdaBoost算法提升弱分类器性能
"""
def adaboost_train_ds(data_arr, labels, num_iter = 40) :
    weak_class_arr = []
    m = np.shape(data_arr)[0]
    D = np.mat(np.ones((m, 1)) / m)  # 初始化权重，样本数量均匀分布
    agg_class_est = np.mat(np.zeros((m, 1)))
    for i in range(num_iter) :
        best_stump, error, best_class_est = build_stump(data_arr, labels, D)
        # print("D:", D.T)
        alpha = float(0.5 * np.log((1.0 - error) / max(error, 1e-16)))
        best_stump['alpha'] = alpha
        weak_class_arr.append(best_stump)
        # print("best_class_est: ", best_class_est.T)
        expon = np.multiply(-1 * alpha * np.mat(labels).T, best_class_est)
        D = np.multiply(D, np.exp(expon))
        D = D / D.sum()
        # 计算AdaBoost误差，当误差为0的时候，退出循环
        agg_class_est += alpha * best_class_est
        # print("agg_class_est: ", agg_class_est.T)
        agg_errors = np.multiply(np.sign(agg_class_est) != np.mat(labels).T, np.ones((m, 1)))  # 计算误差
        error_rate = agg_errors.sum() / m
        # print("total error: ", error_rate)
        if error_rate == 0.0:
            break  # 误差为0，退出循环
    return weak_class_arr, agg_class_est

"""
AdaBoost分类函数
"""
def ada_classify(data_list,classifier_arr) :
    data_matrix = np.mat(data_list)
    m = np.shape(data_matrix)[0]
    agg_class_est = np.mat(np.zeros((m,1)))
    for i in range(len(classifier_arr)) :
        class_est = stump_classify(data_matrix,classifier_arr[i]['dim'],classifier_arr[i]['thresh'],classifier_arr[i]['ineq'])
        agg_class_est += classifier_arr[i]['alpha'] * class_est
        # print(agg_class_est)
    return np.sign(agg_class_est)

"""
pred_strengths - 分类器的预测强度
class_labels - 类别
"""
def plot_ROC(pred_strengths,class_labels) :
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签 
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    cur = (1.0, 1.0)
    ysum = 0.0
    num_pos_class = np.sum(np.array(class_labels) == 1.0)
    ystep = 1 / float(num_pos_class)
    xstep = 1 / float(len(class_labels) - num_pos_class)
    sorted_indicies = pred_strengths.argsort()
    fig = plt.figure()
    fig.clf()
    # “111”表示“1×1网格，第一子图”，“234”表示“2×3网格，第四子图”。
    ax = plt.subplot(111)
    for index in sorted_indicies.tolist()[0] :
        if class_labels[index] == 1.0 :
            delx = 0
            dely = ystep
        else :
            delx = xstep
            dely = 0
            ysum += cur[1]
        ax.plot([cur[0], cur[0] - delx], [cur[1], cur[1] - dely], c='b')  # 绘制ROC
        cur = (cur[0] - delx, cur[1] - dely)
    ax.plot([0, 1], [0, 1], 'b--')
    plt.title('AdaBoost马疝病检测系统的ROC曲线')
    plt.xlabel('假阳率')
    plt.ylabel('真阳率')
    ax.axis([0, 1, 0, 1])
    print('AUC面积为:', ysum * xstep)  # 计算AUC
    plt.show()


