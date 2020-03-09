import numpy as np
import adaboost.adaboost_algorithm as adaboost_algorithm
import machine.constants as consts

def test_build_stump(data_matrix, class_labels) :
    D = np.mat(np.ones((5, 1)) / 5)
    best_stump, min_error, best_class_est = adaboost_algorithm.build_stump(data_matrix, class_labels, D)
    print('best_stump:\n', best_stump)
    print('min_error:\n', min_error)
    print('best_class_est:\n', best_class_est)

def test_adaboost(data_matrix, class_labels) :
    weak_class_arr, agg_class_est = adaboost_algorithm.adaboost_train_ds(data_matrix,class_labels,30)
    print('weak_class_arr :\n',weak_class_arr)
    print('agg_class_est: \n', agg_class_est)
    result = adaboost_algorithm.ada_classify([[0, 0], [5, 5]],weak_class_arr)
    print('result: \n', result)

def test_adaboost_train() :
    data_mat, label_mat = adaboost_algorithm.load_dataset_from_file(consts.FILE_ADABOOST_TRAIN_PATH)
    weak_class_arr, agg_class_est = adaboost_algorithm.adaboost_train_ds(data_mat,label_mat, 10)
    print("weak_class_arr: \n", weak_class_arr)

    test_arr, test_label_arr = adaboost_algorithm.load_dataset_from_file(consts.FILE_ADABOOST_TEST_PATH)
    predictions = adaboost_algorithm.ada_classify(data_mat, weak_class_arr)

    err_arr = np.mat(np.ones((len(data_mat), 1)))
    print('训练集的错误率:%.3f%%' % float(err_arr[predictions != np.mat(label_mat).T].sum() / len(data_mat) * 100))
    predictions = adaboost_algorithm.ada_classify(test_arr, weak_class_arr)
    err_arr = np.mat(np.ones((len(test_arr), 1)))
    print('测试集的错误率:%.3f%%' % float(err_arr[predictions != np.mat(test_label_arr).T].sum() / len(test_arr) * 100))

def test() :
    data_matrix = np.array([[1., 2.1],
                        [1.5, 1.6],
                        [1.3, 1.],
                        [1., 1.],
                        [2., 1.]])
    class_labels = [1.0, 1.0, -1.0, -1.0, 1.0]
    # adaboost_algorithm.show_dataset(datMat,classLabels)
    # test_build_stump(data_matrix, class_labels)
    # test_adaboost(data_matrix, class_labels)

def test_roc() :
    data_mat, label_mat = adaboost_algorithm.load_dataset_from_file(consts.FILE_ADABOOST_TRAIN_PATH)
    weak_class_arr, agg_class_est = adaboost_algorithm.adaboost_train_ds(data_mat, label_mat)
    print("weak_class_arr: \n", weak_class_arr)
    adaboost_algorithm.plot_ROC(agg_class_est.T, label_mat)

if __name__ == '__main__' :
    test()
    test_adaboost_train()
    test_roc()
