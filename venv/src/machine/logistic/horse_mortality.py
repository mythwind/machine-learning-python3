
import logistic.logistic_regres as logistic_regres
import numpy as np

def classify_vector(inx,weights) :
    prob = logistic_regres.sigmoid(sum(inx * weights))
    if prob > 0.5 :
        return 1.0
    return 0.0

def classify_error_rate(train_text,test_text) :
    training_set = []
    training_labels = []
    for line in train_text:
        curr_line = line.strip().split('\t')
        line_arr = []
        for i in range(21):
            line_arr.append(float(curr_line[i]))
        training_set.append(line_arr)
        training_labels.append(float(curr_line[21]))
    training_weights = logistic_regres.stoc_grad_ascent_2(training_set, training_labels, 500)
    error_count = 0
    number_vect = 0.0
    for line in test_text :
        number_vect += 1.0
        curr_line = line.strip().split('\t')
        line_arr = []
        for i in range(21):
            line_arr.append(float(curr_line[i]))
        if int(classify_vector(np.array(line_arr),training_weights)) != int(curr_line[21]) :
            error_count += 1
    error_rate = float(error_count) / number_vect
    print("the error rate of this test is : %f" % (error_rate))
    return error_rate
