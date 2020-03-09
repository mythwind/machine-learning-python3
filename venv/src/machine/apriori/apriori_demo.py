#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @author : mythwind 
# contact : 774202013@qq.com
# @datetime : 2020/3/4 4:19 下午 
# @File : apriori_demo.py
# @desc :

from apriori import apriori_algorithm
from apriori import fpgrouth
from machine import constants


fptree_data = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]


def test_data() :
    dataset = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    c1 = apriori_algorithm.create_c1(dataset)
    print(c1)
    datasetnew = list(map(set, dataset))
    print(datasetnew)
    l1, support_data = apriori_algorithm.scan_d(datasetnew, c1, 0.5)
    print(l1)
    print(support_data)
    print("===============")

    L, support_data = apriori_algorithm.apriori_base(dataset)
    print(L)
    print(support_data)
    # {frozenset({1}): 0.5, frozenset({3}): 0.75, frozenset({4}): 0.25, frozenset({2}): 0.75, frozenset({5}): 0.75,
    # frozenset({1, 3}): 0.5, frozenset({2, 5}): 0.75, frozenset({3, 5}): 0.5, frozenset({2, 3}): 0.5, frozenset({1, 5}): 0.25,
    # frozenset({1, 2}): 0.25, frozenset({2, 3, 5}): 0.5}


def test_mushroom() :
    mashroom_data = [line.split() for line in open('assets/mushroom.dat').readlines()]
    L, support_data = apriori_algorithm.apriori_base(mashroom_data, min_support=0.3)
    for item in L[1] :
        if item.intersection('2'): print(item)
    print("====================")
    for item in L[3]:
        if item.intersection('2'): print(item)


def test_rules() :
    dataset = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    L, support_data = apriori_algorithm.apriori_base(dataset)
    rules = apriori_algorithm.generate_relation_rules(L,support_data, min_conf=0.7)
    print(rules)


def test_fptree():
    root_node = fpgrouth.FPTreeNode('primary', 9, None)
    root_node.children['eye'] = fpgrouth.FPTreeNode('eye', 13, None)
    root_node.display()

    init_set = fpgrouth.create_init_set(fptree_data)
    print("init_set : ", init_set)
    mtree, mheaders = fpgrouth.create_fptree(init_set, 3)
    mtree.display()
    print(mheaders)
    # xxx = fpgrouth.find_prefix_path('x', mheaders['x'][1])
    # print(xxx)
    freq_item = []
    fpgrouth.mine_tree(mtree, mheaders, 3, set([]), freq_item)


def news_fptree():
    parsed_data = [line.split() for line in open(constants.FILE_FPGROUTH_DATA_PATH).readlines()]
    init_set = fpgrouth.create_init_set(parsed_data)
    mtree, mheaders = fpgrouth.create_fptree(init_set, 100000)
    freq_item = []
    fpgrouth.mine_tree(mtree, mheaders, 100000, set([]), freq_item)
    print(freq_item)



if __name__ == '__main__' :
    # test_data()
    # test_mushroom()
    # test_rules()
    # test_fptree()
    news_fptree()

