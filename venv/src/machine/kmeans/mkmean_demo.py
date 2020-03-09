#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @author : mythwind 
# contact : 774202013@qq.com
# @datetime : 2020/3/3 2:59 下午
# @File : mkmean_demo.py
# @desc :
from utils import file_utils
from machine import constants
from kmeans import mkmean


def test_data1() :
    data_mat = file_utils.load_all_dataset(constants.FILE_KMEAN_TEST1_PATH)
    mkmean.plot_orginal_dataset(data_mat)

def test_data2():
    data_mat = file_utils.load_all_dataset(constants.FILE_KMEAN_TEST2_PATH)
    centroids = mkmean.random_center(data_mat,2)
    print(centroids)
    dis = mkmean.distance_eclud(data_mat[0], data_mat[1])
    print(dis)
    print("=============")

    centroids, clust_assing = mkmean.kmeans(data_mat, 3)
    print(centroids)

    mkmean.plot_kmeans(data_mat,centroids,clust_assing)
    #print(clust_assing)


def test_binary_kmeans() :
    data_mat = file_utils.load_all_dataset(constants.FILE_KMEAN_TEST2_PATH)
    cent_list, cluster_assment = mkmean.binary_kmeans(data_mat,3)
    print(cent_list)



def test_club() :
    data_arr = []
    for line in open("assets/places.txt").readlines() :
        line_arr = line.strip().split('\t')
        data_arr.append([float(line_arr[4]), float(line_arr[3])])
    mkmean.cluster_clubs(data_arr)





if __name__ == '__main__' :
    # test_data1()
    # test_data2()
    # test_binary_kmeans()
    test_club()



