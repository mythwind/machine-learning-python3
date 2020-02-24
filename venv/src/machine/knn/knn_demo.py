
import numpy as np
import knn


def classifiy_moives() :
    # 四组二维特征
    group = np.array([[1, 101], [5, 89], [108, 5], [115, 8]])
    # 四组特征的标签
    labels = ['爱情片', '爱情片', '动作片', '动作片']
    # 测试集
    test = [101, 20]
    # kNN分类
    test_class = knn.classify0(test, group, labels, 3)
    # 打印分类结果
    print(test_class)

def classfiy_person() :
    result_list = ['not at all','in small doses','in large doses']
    percent_tats= float(input("percentage of time spent playing video games ?"))
    ffmiles = float(input("frequent flier miles earned per year ?"))
    ice_cream = float(input("liter of ice cream consumed per year ?"))
    dating_mat, dating_labels = knn.file2matrix('./knn/datingTestSet2.txt')
    normal_mat, ranges, min_values = knn.auto_normal(dating_mat)
    inArr = array([ffmiles, percent_tats, ice_cream])
    classfiy_result = knn.classify0((inArr - min_values) / ranges, normal_mat, dating_labels, 3)
    print("You will probably like this person: ", result_list[classfiy_result - 1], "(" + str(classfiy_result) + ")")

def test() :
    group, labels = knn.create_dataset()
    print(group)
    print(labels)
    sort = knn.classify0([0,0],group,labels,3)
    print("distance is %s !"%(sort))
    ## pycharm 中的相对路径不一样，需要在 Run -> Edit Configurations 中查看 Working dorectory
    #dating_mat, dating_labels = knn.file2matrix('./knn/datingTestSet.txt')
    dating_mat, dating_labels = knn.file2matrix('./knn/datingTestSet2.txt')
    print(dating_mat)
    print(dating_labels)
    knn.show_plt(dating_mat,dating_labels)


if __name__ == '__main__':
    #machine()
    #classfiy_person()
    #testvector = knn.img2vector('./knn/testDigits/0_13.txt')
    #print(testvector)
    classifiy_moives()
