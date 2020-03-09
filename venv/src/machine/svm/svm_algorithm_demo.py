import machine.constants as consts
import svm.svm_algorithm as svm_algorithm
import svm.svm_smo as svm_smo
import svm.svm_digits as svm_digits
import numpy as np

def smo_test() :
    data_arr, label_arr = svm_algorithm.load_data_from_file(consts.FILE_SVM_DATA_PATH)
    print(data_arr)
    print(label_arr)
    b, alphas = svm_algorithm.smo_simple(data_arr,label_arr,0.6,0.001,40)
    print(b)
    #print(alphas)
    svm_algorithm.show_classifer(data_arr,label_arr,alphas,b)

def svm_smo_test() :
    data_arr, label_arr = svm_smo.load_data_from_file(consts.FILE_SVM_DATA_PATH)
    b, alphas = svm_smo.smo_p(data_arr, label_arr, 0.6, 0.001, 40)
    w = svm_smo.calc_ws(data_arr, label_arr, alphas)
    svm_algorithm.show_classifer(data_arr, label_arr, alphas, w, b)

def svm_digits_test() :
    k_tup = ('rbf', 10)
    data_arr, labels_arr = svm_digits.load_imges('assets/trainingDigits')
    b, alphas = svm_digits.smo_p(data_arr, labels_arr, 200, 0.0001, 10000, k_tup=('rbf',10))
    dat_mat = np.mat(data_arr)
    label_mat = np.mat(labels_arr).transpose()
    svind = np.nonzero(alphas.A > 0)[0]
    svs = dat_mat[svind]
    label_sv = label_mat[svind]
    print("there are %d support vectors "%(np.shape(svs)[0]))
    m,n = np.shape(dat_mat)
    error_count = 0
    for i in range(m) :
        kernel_eval = svm_digits.kernel_transfer(svs, dat_mat[i,:], k_tup)
        predict = kernel_eval.T * np.multiply(label_sv,alphas[svind]) + b
        if np.sign(predict) != np.sign(labels_arr[i]) :
            error_count += 1
    print("the training error rate is : %f" % (float(error_count) / m))
    data_arr, labels_arr = svm_digits.load_imges('assets/testDigits')
    error_count = 0
    dat_mat = np.mat(data_arr)
    label_mat = np.mat(labels_arr).transpose()
    m, n = np.shape(dat_mat)
    for i in range(m):
        kernel_eval = svm_digits.kernel_transfer(svs, dat_mat[i,:], k_tup)
        predict = kernel_eval.T * np.multiply(label_sv, alphas[svind]) + b
        if np.sign(predict) != np.sign(labels_arr[i]):
            error_count += 1
    print("the test error rate is : %f" % (float(error_count) / m))


if __name__ == '__main__' :
    #smo_test()
    #svm_smo_test()
    svm_digits_test()

    dm = [[1,2,3,4],[11,12,13,14],[21,22,23,24]]
    print(dm)
    dm = np.mat(dm)
    print(dm)
    print("======")
    print(dm[2,:])
    print(dm[2:])

    print(np.zeros((2,5)))


