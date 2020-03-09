#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @author : mythwind 
# contact : 774202013@qq.com
# @datetime : 2020/3/5 9:38 上午 
# @File : fpgrouth.py
# @desc :


"""
name：节点元素名称，在构造时初始化为给定值
count：出现次数，在构造时初始化为给定值
node_link：指向下一个相似节点的指针，默认为None
parent：指向父节点的指针，在构造时初始化为给定值
children：指向子节点的字典，以子节点的元素名称为键，指向子节点的指针为值，初始化为空字典
"""
class FPTreeNode :
    def __init__(self, name_val, num_occur, parent_node):
        self.name = name_val
        self.count = num_occur
        self.node_link = None
        self.parent = parent_node
        self.children = {}

    def increase(self, num_occur):
        """
        增加节点的出现次数值
        :param num_occur:
        :return:
        """
        self.count += num_occur

    def display(self, ind=1):
        """
        输出节点和子节点的FP树结构
        :param ind:
        :return:
        """
        print('FPTreeNode...:', ' ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.display(ind + 1)




def create_init_set(dataset):
    result_dict = {}
    for trans in dataset:
        result_dict[frozenset(trans)] = 1
    return result_dict


def create_fptree(dataset, min_sup=1):
    # 第一次遍历数据集，创建头指针表
    header_table = {}
    for trans in dataset:
        for item in trans:
            header_table[item] = header_table.get(item, 0) + dataset[trans]
    # print("header_table: \n", header_table)
    # 移除不满足最小支持度的元素项
    for k in list(header_table.keys()):
        if header_table[k] < min_sup:
            del(header_table[k])
    # 空元素集，返回空
    freq_item_set = set(header_table.keys())
    if len(freq_item_set) == 0:
        return None, None
    # 增加一个数据项，用于存放指向相似元素项指针
    for k in header_table:
        header_table[k] = [header_table[k], None]
    # 创建树的根节点
    result_tree = FPTreeNode('Null Set', 1, None)
    # 第二次遍历数据集，创建FP树
    for trans_set, count in dataset.items():
        local_data = {}
        for item in trans_set:
            if item in freq_item_set:
                local_data[item] = header_table[item][0]  # 注意这个[0]，因为之前加过一个数据项
        # print("local_data======:", local_data)
        if len(local_data) > 0:
            ordered_items = [v[0] for v in sorted(local_data.items(), key=lambda p: p[1], reverse=True)]  # 排序
            update_fptree(ordered_items, result_tree, header_table, count)  # 更新FP树
    return result_tree, header_table


def update_fptree(items, tree, header_table, count):
    if items[0] in tree.children:
        # 有该元素项时计数值+1
        tree.children[items[0]].increase(count)
    else:
        # 没有这个元素项时创建一个新节点
        tree.children[items[0]] = FPTreeNode(items[0], count, tree)
        # 更新头指针表或前一个相似元素项节点的指针指向新节点
        if header_table[items[0]][1] == None:
            header_table[items[0]][1] = tree.children[items[0]]
        else:
            update_fpheader(header_table[items[0]][1], tree.children[items[0]])
    if len(items) > 1:
        # 对剩下的元素项迭代调用updateTree函数
        update_fptree(items[1::], tree.children[items[0]], header_table, count)



def update_fpheader(test_node, target_node):
    """
    处理链表指针，获取头指针表中该元素项对应的单链表的尾节点，然后将其指向新节点targetNode
    :param test_node:
    :param target_node:
    :return:
    """
    while test_node != None and test_node.node_link != None:
        test_node = target_node.node_link
    if test_node != None :
        test_node.node_link = target_node


def ascend_tree(leaf_node, prefix_path):
    """
    根据节点位置，查找父节点，一直找到根节点停止
    :param leaf_node:
    :param prefix_path:
    :return:
    """
    if leaf_node.parent != None:
        prefix_path.append(leaf_node.name)
        ascend_tree(leaf_node.parent, prefix_path)



def find_prefix_path(base_freqs, tree_node):
    """
    为给定元素项生成一个条件模式基（前缀路径）,这通过访问树中所有包含给定元素项的节点来完成。
    :param base_freqs:
    :param tree_node:
    :return:
    """
    result_freqs = {}
    while tree_node != None:
        prefix_path = []
        ascend_tree(tree_node, prefix_path)
        if len(prefix_path) > 1:
            result_freqs[frozenset(prefix_path[1:])] = tree_node.count
        tree_node = tree_node.node_link
    return result_freqs



def mine_tree(tree, header_table, min_sup, prefix, freq_item):
    """
    输入：我们有当前数据集的FP树（inTree，headerTable）
    1. 初始化一个空列表preFix表示前缀
    2. 初始化一个空列表freqItemList接收生成的频繁项集（作为输出）
    3. 对headerTable中的每个元素basePat（按计数值由小到大），递归：
            3.1 记basePat + preFix为当前频繁项集newFreqSet
            3.2 将newFreqSet添加到freqItemList中
            3.3 计算t的条件FP树（myCondTree、myHead）
            3.4 当条件FP树不为空时，继续下一步；否则退出递归
            3.4 以myCondTree、myHead为新的输入，以newFreqSet为新的preFix，外加freqItemList，递归这个过程
    :param tree:
    :param header_table:
    :param min_sup:
    :param prefix:
    :param freq_item:
    :return:
    """
    if len(header_table) ==0:
        return None
    bigL = [v[0] for v in sorted(header_table.items(), key=lambda p: p[1][0])]
    for basePat in bigL:
        newFreqSet = prefix.copy()
        newFreqSet.add(basePat)
        freq_item.append(newFreqSet)
        condPattBases = find_prefix_path(basePat, header_table[basePat][1])
        mcond_ree, mheaders = create_fptree(condPattBases, min_sup)
        if mheaders != None:
            # 用于测试
            print('conditional tree for:', newFreqSet)
            mcond_ree.display()
            mine_tree(mcond_ree, mheaders, min_sup, newFreqSet, freq_item)


