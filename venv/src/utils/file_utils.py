import numpy as np


def load_dataset_from_file(filename) :
    """
    从文件读取数据，得到数据集和分类集
    :param filename: 文件路径
    :return: 返回数据集合和分类集合
    """
    # 读取数据集列
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


def load_all_dataset(filename) :
    """
    读取全部数据保存在 data_mat
    :param filename:
    :return:
    """
    data_mat = []
    fr = open(filename)
    for line in fr.readlines() :
        curr_line = line.strip().split('\t')
        flt_line = list(map(float,curr_line))
        data_mat.append(flt_line)
    return data_mat


def load_map_datamat(filename, delim='\t') :
    """
    读取全部数据保存在matrix, 数据是 map
    :param filename: 数据文件路径
    :param delim: 数据文件分隔符
    :return: 矩阵式数据
    """
    str_arr = [line.strip().split(delim) for line in open(filename).readlines()]
    data_arr = [list(map(float, line)) for line in str_arr]
    return np.mat(data_arr)


