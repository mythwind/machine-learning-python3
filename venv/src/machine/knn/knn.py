
import numpy as np
import operator
import matplotlib
import matplotlib.pyplot as plt

def create_dataset() :
    group = np.array([[1.0,1.1],[1.0,1.0],[0,0],[0.1,0.1]])
    labels = ['A','A','B','B']
    return group, labels

'''
计算点到点的距离: 欧氏距离(也称欧几里德度量)
A(1,0,0,1)
B(7,6,9,4)
S**2 = (1-7)**2 + (0-6)**2 + (0-9)**2 + (1-4)**2

'''
def classify0(intx,dataset,labels,k) :
    # numpy函数shape[0]返回dataSet的行数
    dataset_size = dataset.shape[0]
    # 在列向量方向上重复inX共1次(横向)，行向量方向上重复inX共dataSetSize次(纵向)
    diff_mat = np.tile(intx, (dataset_size, 1)) - dataset
    sq_diff_mat = diff_mat ** 2 ## 计算平方值
    # sum()所有元素相加，sum(0)列相加，sum(1)行相加
    sq_distances = sq_diff_mat.sum(axis=1)
    #开方，计算出距离
    distances = sq_distances ** 0.5
    # 返回distances中元素从小到大排序后的索引值
    sorted_dist_indicies = distances.argsort()
    print(sorted_dist_indicies)
    # 定义一个记录类别次数的字典
    class_count = {}
    for i in range(k) :
        vote_label = labels[sorted_dist_indicies[i]]
        class_count[vote_label] = class_count.get(vote_label, 0) + 1
    #  python 3.5, iteritems 改成 items
    # key=operator.itemgetter(1)根据字典的值进行排序
    # key=operator.itemgetter(0)根据字典的键进行排序
    # reverse降序排序字典
    sort_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return sort_class_count[0][0]

'''
读取文件数据转化为matrix
'''
def file2matrix(filename) :
    fr = open(filename)
    array_lines = fr.readlines()
    number_of_lines = len(array_lines)
    return_mat = np.zeros((number_of_lines, 3)) ##创建矩阵
    class_label_vector = []
    index = 0
    for line in array_lines :
        line = line.strip()     #截取所有回车字符
        list_from_line = line.split("\t")   #截取每行\t数据个数
        return_mat[index, :] = list_from_line[0 : 3]    ##文本前3个元素放入 return_mat
        #class_label_vector.append(int(list_from_line[-1]))  # -1 表示最后一个元素
        class_label_vector.append(int(list_from_line[-1]))  # -1 表示最后一个元素
        index += 1
    return return_mat, class_label_vector

'''
数值归一化：
    在处理不同取值范围时候，通常采用数值归一化
'''
def auto_normal(dataset) :
    min_value = dataset.min(0)  #从列中选取最小值，而不是选取当前行的最小值
    max_value = dataset.max(0)
    ranges = max_value - min_value
    normal_dataset = np.zeros(np.shape(dataset))
    m = dataset.shape[0]
    normal_dataset = dataset - np.tile(min_value, (m,1))
    normal_dataset = normal_dataset / np.tile(ranges, (m,1))
    return normal_dataset, ranges, min_value

'''
使用matplotlib画二维扩散图
'''
def show_plt(data_mat,data_labels) :
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(data_mat[:,1],data_mat[:,2],15.0*np.array(data_labels),15.0*np.array(data_labels))
    plt.show()


def img2vector(filename) :
    ## zeros 产生一个1行1024列的数组0矩阵
    return_vect = np.zeros((1,1024))
    fr = open(filename)
    for i in range(32) :    # 读取文件的前32行
        linestr = fr.readline()
        for j in range(32) :   # 读取每行前32个字符
            return_vect[0, 32 * i + j] = int(linestr[j])
    return return_vect


