
import decison_tree.decision_tree as decision_tree
import machine.constants as consts

def test() :
    dataset = [[0, 0, 0, 0, 'no'],  # 数据集
               [0, 0, 0, 1, 'no'],
               [0, 1, 0, 1, 'yes'],
               [0, 1, 1, 0, 'yes'],
               [0, 0, 0, 0, 'no'],
               [1, 0, 0, 0, 'no'],
               [1, 0, 0, 1, 'no'],
               [1, 1, 1, 1, 'yes'],
               [1, 0, 1, 2, 'yes'],
               [1, 0, 1, 2, 'yes'],
               [2, 0, 1, 2, 'yes'],
               [2, 0, 1, 1, 'yes'],
               [2, 1, 0, 1, 'yes'],
               [2, 1, 0, 2, 'yes'],
               [2, 0, 0, 0, 'no']]
    labels = ['年龄', '有工作', '有自己的房子', '信贷情况']  # 分类属性
    feat_labels = []
    #print(decision_tree.calc_shanon_entropy(dataset))
    #print("最优特征索引值:" + str(decision_tree.choose_best_feature_to_split(dataset)))
    mtree = decision_tree.create_tree(dataset, labels, feat_labels)
    print(consts.PI)
    decision_tree.store_tree(mtree,consts.FILE_TREE_CLFS_PATH)
    print(decision_tree.grab_tree(consts.FILE_TREE_CLFS_PATH))
    decision_tree.create_plot(mtree)

    result = decision_tree.classify(mtree, feat_labels, [0,1])
    if result == 'yes':
        print('放贷')
    if result == 'no':
        print('不放贷')

def lenses() :
    fr = open(consts.FILE_TREE_LENSES_PATH)
    lenses = [instr.strip().split('\t') for instr in fr.readlines()]
    print(lenses)
    labels = ['age','prescript','astigmatic','tearRate']
    feat_labels = []
    lenses_tree = decision_tree.create_tree(lenses, labels, feat_labels)
    print(lenses_tree)
    #decision_tree.create_plot(lenses_tree)

if __name__ == '__main__' :
    #machine()
    lenses()
