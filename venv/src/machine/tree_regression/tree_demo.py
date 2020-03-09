from machine import constants
from utils import file_utils
from tree_regression import tree_regres
from tree_regression import plt_and_tk
import numpy as np


def test_original():
    data_mat = file_utils.load_all_dataset(constants.FILE_TREE_EX00_PATH)
    tree_regres.plot_ex00_dataset(data_mat)

    data_mat = file_utils.load_all_dataset(constants.FILE_TREE_EX0_PATH)
    tree_regres.plot_ex0_dataset(data_mat)

    data_mat = file_utils.load_all_dataset(constants.FILE_TREE_EX2_PATH)
    tree_regres.plot_ex00_dataset(data_mat)

    # mat0, mat1 = tree_regres.bin_split_dataset(data_mat, 1, 0.5)
    # print('原始集合:\n', data_mat)
    # print('mat0:\n', mat0)
    # print('mat1:\n', mat1)


def test_tree() :
    data_mat = file_utils.load_all_dataset(constants.FILE_TREE_EX0_PATH)
    data_mat = np.mat(data_mat)
    result = tree_regres.create_tree(data_mat)
    print(result)

    data_mat = file_utils.load_all_dataset(constants.FILE_TREE_EX2_PATH)
    data_mat = np.mat(data_mat)
    tree = tree_regres.create_tree(data_mat)
    print(tree)
    test_data = file_utils.load_all_dataset(constants.FILE_TREE_EX2TEST_PATH)
    test_data = np.mat(test_data)
    new_tree = tree_regres.prune(tree,test_data)
    print("new_tree: \n", new_tree)

def test_model_tree() :
    data_arr = file_utils.load_all_dataset(constants.FILE_TREE_EXP2_PATH)

    data_mat = np.mat(data_arr)
    tree = tree_regres.create_tree(data_mat, tree_regres.model_leaf, tree_regres.model_error, (1,10))
    print(tree)

    tree_regres.plot_model_tree(data_arr, tree)


def test_diff_tree() :
    test_arr = file_utils.load_all_dataset(constants.FILE_TREE_BIKE_TEST_PATH)
    train_arr = file_utils.load_all_dataset(constants.FILE_TREE_BIKE_TRAIN_PATH)
    tree = tree_regres.create_tree(np.mat(train_arr), ops=(1,20))
    yhat = tree_regres.create_forecast(tree, np.mat(test_arr)[:,0])
    ret = np.corrcoef(yhat, np.mat(test_arr)[:,1], rowvar=0)[0,1]
    print("树回归的预测结果：", ret)

    ws,X,Y = tree_regres.linear_solve(np.mat(train_arr))
    for i in range(np.shape(np.mat(test_arr))[0]) :
        yhat[i] = np.mat(test_arr)[i,0] * ws[1,0] + ws[0,0]
    ret = np.corrcoef(yhat, np.mat(test_arr)[:,1], rowvar=0)[0,1]
    print("线性回归的预测结果：", ret)

def test_tkinter() :
    tree_regres.test_tkinter()

if __name__ == '__main__':
    ## 前面两行；第三行开始
    # print('原始集合1111:\n', data_mat[:2])
    # print('原始集合1111:\n', data_mat[2:])
    # test_original()
    # test_tree()
    # test_model_tree()
    # 回归树与标准回归的比较
    # test_diff_tree()
    # test_tkinter()

    plt_and_tk.test_tkinter()
