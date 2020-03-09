#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @author : mythwind 
# contact : 774202013@qq.com
# @datetime : 2020/3/4 3:54 下午 
# @File : apriori_algorithm.py
# @desc :


'''
频繁项集：frequent item
    首先会生成所有单个物品的项集列表
    扫描交易记录来查看哪些项集满足最小支持度要求，那些不满足最小支持度的集合会被去掉
    对剩下的集合进行组合以生成包含两个元素的项集
    接下来重新扫描交易记录，去掉不满足最小支持度的项集，重复进行直到所有项集都被去掉
'''



def create_c1(dataset) :
    """
    c1是大小为1的所有候选项集的集合, 将所有元素转换为frozenset型字典，存放到列表中
    相当于总记录数据
    :param dataset:
    :return:
    """
    c1 = []
    for transaction in dataset :
        for item in transaction :
            # 此处每次添加是添加一个单一数据的列表哦
            if not [item] in  c1 :
                c1.append([item])
    c1.sort()
    # 使用frozenset是为了后面可以将这些值作为字典的键
    # frozenset一种不可变的集合，set可变集合
    return list(map(frozenset, c1))



def scan_node(dataset, ck, min_support) :
    """
    用于从c1生成l1
    :param dataset:  数据集
    :param ck: 候选项集合，单个数据集合 {{1},{2},{3}, ...}
    :param min_support: 感兴趣项集的最小支持度
    :return:
        result_list : 频繁项集
        support_data：数据集的支持度
    """
    sscnt = {}
    for tid in dataset:
        for can in ck:
            # 判断can是否是tid的《子集》 （这里使用子集的方式来判断两者的关系）
            if can.issubset(tid):
                # 统计该值在整个记录中满足子集的次数（以字典的形式记录，frozenset为键）
                if not can in sscnt:
                    sscnt[can] = 1
                else :
                    sscnt[can] +=  1
    num_items = float(len(dataset))
    result_list = []  # 重新记录满足条件的数据值（即支持度大于阈值的数据）
    support_data = {}  # 每个数据值(单个元素)的支持度
    for key in sscnt:
        # 计算支持度。
        support = sscnt[key] / num_items
        # 支持度大于最小支持度，数据加入支持度列表
        if support >= min_support:
            result_list.insert(0, key)
        support_data[key] = support
    return result_list, support_data  # 排除不符合支持度元素后的元素 每个元素支持度


def apriori_gen(frequent_item, k) :
    """
    :param lk: 频繁项集列表   Frequent items
    :param k: 频繁项集元素个数, k从2开始是因为单个元素的频繁项集已经在首次调用 scan_node 处理过
    :return:
    """
    result_list = []
    lenlk = len(frequent_item)
    for i in range(lenlk):
        for j in range(i + 1, lenlk):
            l1 = list(frequent_item[i])[: k - 2]
            l2 = list(frequent_item[j])[: k - 2]
            l1.sort()
            l2.sort()
            if l1 == l2 :
                result_list.append(frequent_item[i] | frequent_item[j])
    return result_list


def apriori_base(dataset, min_support=0.5):
    c1 = create_c1(dataset)
    dataset_arr = list(map(set, dataset))
    l1, support_data = scan_node(dataset_arr, c1, min_support)
    l = [l1]
    k = 2
    while len(l[k - 2]) > 0 :# 若仍有满足支持度的集合则继续做关联分析
        ck = apriori_gen(l[k - 2], k)
        lk, support_k = scan_node(dataset_arr, ck, min_support)
        # 更新字典（把新出现的集合:支持度加入到supportData中）
        support_data.update(support_k)
        l.append(lk)
        k += 1
    return l, support_data



def generate_relation_rules(frequent_arr, support_data, min_conf=0.7):
    """
    获取关联规则的封装函数
    :param L:
    :param support_data:
    :param min_conf:
    :return:
    """
    big_rule_list = []
    # 从为2个元素的集合开始
    for i in range(1, len(frequent_arr)):
        for freqset in frequent_arr[i]:
            # 只包含单个元素的集合列表
            H1 = [frozenset([item]) for item in freqset]  # frozenset({2, 3}) 转换为 [frozenset({2}), frozenset({3})]
            # 如果集合元素大于2个，则需要处理才能获得规则
            if (i > 1):
                rules_from_conseq(freqset, H1, support_data, big_rule_list, min_conf)  # 集合元素 集合拆分后的列表 。。。
            else:
                calc_confidence(freqset, H1, support_data, big_rule_list, min_conf)
    return big_rule_list


def calc_confidence(freqset, H, support_data, brl, min_conf=0.7):
    """
    对规则进行评估 获得满足最小置信度的关联规则
    :param freqset:
    :param H:
    :param support_data:
    :param brl:
    :param min_conf:
    :return:
    """
    prunedH = []  # 创建一个新的列表去返回
    for conseq in H:
        conf = support_data[freqset] / support_data[freqset - conseq]  # 计算置信度
        if conf >= min_conf:
            print(freqset - conseq, '-->', conseq, 'conf:', conf)
            brl.append((freqset - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH



def rules_from_conseq(freqset, H, support_data, brl, min_conf=0.7):
    """
    生成候选规则集合
    :param freqset:
    :param H:
    :param support_data:
    :param brl:
    :param min_conf:
    :return:
    """
    m = len(H[0])
    if (len(freqset) > (m + 1)):  # 尝试进一步合并
        merged = apriori_gen(H, m + 1)  # 将单个集合元素两两合并
        merged = calc_confidence(freqset, merged, support_data, brl, min_conf)
        if (len(merged) > 1):  # need at least two sets to merge
            rules_from_conseq(freqset, merged, support_data, brl, min_conf)



