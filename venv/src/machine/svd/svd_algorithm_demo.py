#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @author : mythwind 
# contact : 774202013@qq.com
# @datetime : 2020/3/9 10:26 上午 
# @File : svd_algorithm_demo.py
# @desc :
import numpy as np
from svd import svd_algorithm


data = [
    [1, 1, 1, 0, 0],
    [2, 2, 2, 0, 0],
    [1, 1, 1, 0, 0],
    [5, 5, 5, 0, 0],
    [1, 1, 0, 2, 2],
    [0, 0, 0, 3, 3],
    [0, 0, 0, 1, 1]
]

data_complex = [[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
           [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
           [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
           [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
           [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
           [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
           [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
           [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
           [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
           [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
           [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]



def test_data():
    U, sigma, vt = np.linalg.svd([[1, 1], [7, 7]])
    # sigma 仅仅返回矩阵的对角元素（因为除对角元素之外其他元素均为0）
    print(U, sigma, vt)

    print("===============")
    U, sigma, vt = np.linalg.svd(data)
    # 前面3个值比其他值大很多，确定要保留的奇异值的数目有很多启发式的策略，其中一个典型的做法是保留矩阵中90%的能量信息
    # 当矩阵上有上万的奇异值时，那么就保留前面的2000或3000个。在任何数据集上，都不能保证前3000个奇异值能够包含90%的能量信息，但在实际中更容易实施。
    print(sigma)

    sig3 = np.mat([[sigma[0], 0, 0],[0, sigma[1], 0],[0, 0, sigma[2]]])
    result = U[:, :3] * sig3 * vt[:3, :]
    print(result)


def test_similar():
    data_mat = np.mat(data)
    similar = svd_algorithm.euclid_similar(data_mat[:,0], data_mat[:,4])
    print("欧几里得相似度：", similar)
    similar = svd_algorithm.pearson_similar(data_mat[:, 0], data_mat[:, 4])
    print("皮尔逊相似度：", similar)
    similar = svd_algorithm.cosine_similar(data_mat[:, 0], data_mat[:, 4])
    print("余弦相似度：", similar)

    data_mat[0, 1] = data_mat[0, 0] = data_mat[1, 0] = data_mat[2, 0] = 4
    data_mat[3,3] = 2

    result = svd_algorithm.recommend_engine(data_mat, 2)
    print(result)
    svd_algorithm.recommend_engine(data_mat, 2, sim_meas=svd_algorithm.euclid_similar)
    print(result)
    svd_algorithm.recommend_engine(data_mat, 2, sim_meas=svd_algorithm.pearson_similar)
    print(result)


def test_complex_data():
    data_mat = np.mat(data_complex)
    result = svd_algorithm.recommend_engine(data_mat, 1, estimated_method=svd_algorithm.svd_estimated)
    print(result)
    result = svd_algorithm.recommend_engine(data_mat, 1, estimated_method=svd_algorithm.svd_estimated, sim_meas=svd_algorithm.pearson_similar)
    print(result)

    # 构建一个列表myl
    myl = []
    # 打开文本文件，以数值方式读入字符
    for line in open("assets/0_5.txt").readlines():
        newRow = []
        for i in range(32):
            newRow.append(int(line[i]))
        myl.append(newRow)
    file_data = np.mat(myl)

    svd_algorithm.image_compress(file_data,2)


if __name__ == '__main__':
    # test_data()
    # test_similar()
    test_complex_data()

    # data_x = np.mat(data)
    # print(data_x)
    # print(data_x[:2])   # 矩阵的前面两行
    # print(data_x[:,2])  # 矩阵的第二列 ？
    # print(data_x[:,:2])  # 矩阵的前两列 ？


