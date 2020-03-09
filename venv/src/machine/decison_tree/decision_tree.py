import matplotlib.pyplot as plt
import math
import pickle
import operator


def calc_shanon_entropy(dataset):
    """
    计算香农熵
    H = -sum(p(xi)log2p(xi))
    p(xi) = 统计xi出现次数 / 总数
    """
    entropy_size = len(dataset)
    # 保存每个标签(Label)出现次数的字典
    label_counts = {}
    # 对每组特征向量进行统计
    for feat_vec in dataset:
        curr_label = feat_vec[-1]  # 提取标签(Label)信息
        if curr_label not in label_counts.keys():
            label_counts[curr_label] = 0
        label_counts[curr_label] += 1
    # 经验熵(香农熵)
    shanon_entropy = 0.0
    for key in label_counts:
        # 选择该标签(Label)的概率
        prob = float(label_counts[key]) / entropy_size
        shanon_entropy -= prob * math.log(prob, 2)
    return shanon_entropy


"""
函数说明:按照给定特征划分数据集
    dataSet - 待划分的数据集
    axis - 划分数据集的特征
    value - 需要返回的特征的值
"""


def split_dataset(dataset, axis, value):
    result_dataset = []
    for feat_vec in dataset:
        if feat_vec[axis] == value:
            reduced_feat = feat_vec[:axis]
            reduced_feat.extend(feat_vec[axis + 1:])
            result_dataset.append(reduced_feat)
    return result_dataset


'''
选择最优特征
bestFeature - 信息增益最大的(最优)特征的索引值
'''


def choose_best_feature_to_split(dataset):
    feature_size = len(dataset[0]) - 1
    base_entropy = calc_shanon_entropy(dataset)  # 计算数据集的香农熵
    best_info_gain = 0.0  # 信息增益
    best_feature_idx = -1
    for i in range(feature_size):
        # 获取dataSet的第i个所有特征
        feat_list = [example[i] for example in dataset]
        unique_values = set(feat_list)
        # print("======特征值",i,"======", unique_values)
        new_entropy = 0.0
        for val in unique_values:
            sub_dataset = split_dataset(dataset, i, val)
            # print("======子集======", sub_dataset)
            # 计算子集的概率
            prob = len(sub_dataset) / float(len(dataset))
            new_entropy += prob * calc_shanon_entropy(sub_dataset)
        info_gain = base_entropy - new_entropy
        print("第%d个特征的增益为%.3f，%.3f，%.3f" % (i, info_gain, base_entropy, new_entropy))  # 打印每个特征的信息增益
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_feature_idx = i
    return best_feature_idx


def majority_count(class_list):
    """
    统计class_list中出现此处最多的元素(类标签)
    """
    class_count = {}
    for vote in class_list:
        if vote not in class_count.keys():
            class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]


def create_tree(dataset, labels, feature_labels):
    '''
    创建决策树
    labels  ： 全部标签
    feature_labels : 特征标签放入list
    '''
    # 取分类标签(是否放贷:yes or no)
    class_list = [example[-1] for example in dataset]
    # 如果类别完全相同则停止继续划分
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]
    if len(dataset[0]) == 1:  # 遍历完所有特征时返回出现次数最多的类标签
        return majority_count(class_list)
    if len(labels) == 0:  # 遍历完所有特征时返回出现次数最多的类标签
        return majority_count(class_list)
    best_feature = choose_best_feature_to_split(dataset)
    best_feature_label = labels[best_feature]
    feature_labels.append(best_feature_label)
    my_tree = {best_feature_label: {}}  # 根据最优特征的标签生成树
    del (labels[best_feature])  # 删除已经使用特征标签
    feat_values = [example[best_feature] for example in dataset]  # 得到训练集中所有最优特征的属性值
    unique_vals = set(feat_values)  # 去掉重复的属性值
    for value in unique_vals:  # 遍历特征，创建决策树。
        my_tree[best_feature_label][value] = create_tree(split_dataset(dataset, best_feature, value), labels,feature_labels)
    return my_tree


def get_tree_leafs_num(tree_name):
    leafs_num = 0
    # first = tree_name.keys()[0]
    # python 3 中myTree.keys()返回的是dict_keys,不在是list,所以不能使用myTree.keys()[0]的方法获取结点属性，可以使用list(myTree.keys())[0]
    first = next(iter(tree_name))
    second_dict = tree_name[first]
    for key in second_dict.keys():
        # 测试该结点是否为字典，如果不是字典，代表此结点为叶子结点
        if type(second_dict[key]).__name__ == 'dict':
            leafs_num += get_tree_leafs_num(second_dict[key])
        else:
            leafs_num += 1
    return leafs_num


def get_tree_depth(tree_name):
    max_depth = 0
    first = next(iter(tree_name))
    second_dict = tree_name[first]
    for key in second_dict.keys():
        # 测试该结点是否为字典，如果不是字典，代表此结点为叶子结点
        if type(second_dict[key]).__name__ == 'dict':
            this_depth = 1 + get_tree_leafs_num(second_dict[key])
        else:
            this_depth = 1
        if this_depth > max_depth:
            max_depth = this_depth
    return max_depth


def plot_mid_text(center_point, parent_point, node_text):
    xmid = center_point[0] + (parent_point[0] - center_point[0]) / 2
    ymid = center_point[1] + (parent_point[1] - center_point[1]) / 2
    create_plot.ax1.text(xmid, ymid, node_text, va="center", ha="center", rotation=30)


def plot_node(node_text, center_point, parent_point, node_type):
    arrow_args = dict(arrowstyle="<-")  # 定义箭头格式
    # font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)  # 设置中文字体
    create_plot.ax1.annotate(node_text, xy=parent_point, xycoords='axes fraction',  # 绘制结点
                             xytext=center_point, textcoords='axes fraction',
                             va="center", ha="center", bbox=node_type, arrowprops=arrow_args)


def plot_tree(tree, parent_point, node_text):
    decision_node = dict(boxstyle="sawtooth", fc="0.8")  # 设置结点格式
    leaf_node = dict(boxstyle="round4", fc="0.8")  # 设置叶结点格式
    numLeafs = get_tree_leafs_num(tree)  # 获取决策树叶结点数目，决定了树的宽度
    # depth = get_tree_depth(tree)  # 获取决策树层数
    first_dict = next(iter(tree))  # 下个字典
    center_point = (plot_tree.xOff + (1.0 + float(numLeafs)) / 2.0 / plot_tree.totalW, plot_tree.yOff)  # 中心位置
    plot_mid_text(center_point, parent_point, node_text)  # 标注有向边属性值
    plot_node(first_dict, center_point, parent_point, decision_node)  # 绘制结点
    second_dict = tree[first_dict]
    plot_tree.yOff = plot_tree.yOff - 1.0 / plot_tree.totalD
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            plot_tree(second_dict[key], center_point, str(key))
        else:
            plot_tree.xOff = plot_tree.xOff + 1.0 / plot_tree.totalW
            plot_node(second_dict[key], (plot_tree.xOff, plot_tree.yOff), center_point, leaf_node)
            plot_mid_text((plot_tree.xOff, plot_tree.yOff), center_point, str(key))
    plot_tree.yOff = plot_tree.yOff + 1.0 / plot_tree.totalD


def create_plot(in_tree):
    fig = plt.figure(1, facecolor='white')
    # plt.rcParams['font.sans-serif'] = ['Arial Unicode MS'] # 字体需要选择pc系统有的字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    fig.clf()
    # 清空fig
    axprops = dict(xticks=[], yticks=[])
    # 参数为111，即中间没有逗号隔开的意思。
    create_plot.ax1 = plt.subplot(111, frameon=False, **axprops)  # 去掉x、y轴
    plot_tree.totalW = float(get_tree_leafs_num(in_tree))  # 获取决策树叶结点数目
    plot_tree.totalD = float(get_tree_depth(in_tree))  # 获取决策树层数
    plot_tree.xOff = -0.5 * plot_tree.totalW
    plot_tree.yOff = 1.0
    plot_tree(in_tree, (0.5, 1.0), '')
    plt.show()


"""
决策树分类
"""


def classify(input_tree, feat_labels, test_vec):
    first_dict = next(iter(input_tree))
    second_dict = input_tree[first_dict]
    feat_index = feat_labels.index(first_dict)
    for key in second_dict.keys():
        if test_vec[feat_index] == key:
            if type(second_dict[key]).__name__ == 'dict':
                class_labels = classify(second_dict[key], feat_labels, test_vec)
            else:
                class_labels = second_dict[key]
    return class_labels


def store_tree(input_tree, filename):
    """
    存储决策树
    """
    with open(filename, 'wb') as fw:
        pickle.dump(input_tree, fw)
    fw.close()


def grab_tree(filename):
    """
    读取决策树
    """
    fr = open(filename, 'rb')
    return pickle.load(fr)
