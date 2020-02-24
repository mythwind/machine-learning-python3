
import machine.constants as const
import logistic.logistic_regres as logistic_regres
import logistic.horse_mortality as horse_mortality

def logistic() :
    data_mat = []
    label_mat = []
    fr = open(const.FILE_LOGISTIC_DATA_PATH)
    for line in fr.readlines() :
        line_arr = line.strip().split()
        # print(line_arr)
        data_mat.append([1.0,float(line_arr[0]),float(line_arr[1])])
        label_mat.append(int(line_arr[2]))
    fr.close()
    weights = logistic_regres.grad_ascent(data_mat, label_mat)
    print("weights:",weights)
    #getA()函数与mat()函数的功能相反，是将一个numpy矩阵转换为数组
    logistic_regres.plot_best_fit(data_mat,label_mat,weights)

    weights = logistic_regres.stoc_grad_ascent_0(data_mat, label_mat)
    print("weights:", weights)
    # getA()函数与mat()函数的功能相反，是将一个numpy矩阵转换为数组
    logistic_regres.plot_best_fit(data_mat, label_mat, weights)

    weights1, weights_array1 = logistic_regres.stoc_grad_ascent_1(data_mat, label_mat)
    weights2, weights_array2 = logistic_regres.grad_ascent_1(data_mat, label_mat)
    logistic_regres.plot_weights(weights_array1, weights_array2)

def horse_forecast() :
    fr_train = open(const.FILE_LOGISTIC_HORSE_TRAINING_PATH)
    fr_test = open(const.FILE_LOGISTIC_HORSE_TEST_PATH)

    train_text = fr_train.readlines()
    test_text = fr_test.readlines()

    fr_train.close()
    fr_test.close()

    num_test = 10
    err_sum = 0.0
    for i in range(num_test) :
        err_sum += horse_mortality.classify_error_rate(train_text,test_text)
    print("after %d iterations the average error rate is : %f" % (num_test, err_sum / float(num_test)))


if __name__ == '__main__' :
    # logistic()
    horse_forecast()