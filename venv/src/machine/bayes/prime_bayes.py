
import numpy as np
import operator
import random

"""
将切分的实验样本词条整理成不重复的词条列表，也就是词汇表
"""
def create_vocab_list(dataset) :
    vocab_set = set([])
    for doc in dataset :
        vocab_set = vocab_set | set(doc) #取并集
    return list(vocab_set)

"""
根据vocabList词汇表，将inputSet向量化，向量的每个元素为1或0
词集模型
"""
def setofwords_vec(vocab_list, input_set):
    return_vec = [0] * len(vocab_list)
    for word in input_set :
        if word in vocab_list :
            return_vec[vocab_list.index(word)] = 1
        else :
            print("the word: %s is not in my Vocabulary!" % word)
    return return_vec

"""
朴素贝叶斯分类器训练函数
    trainMatrix - 训练文档矩阵，即setOfWords2Vec返回的returnVec构成的矩阵
    trainCategory - 训练类别标签向量，即loadDataSet返回的classVec
"""
def train_nb0(train_matrix,train_category) :
    train_docs = len(train_matrix)
    words_cnt = len(train_matrix[0])
    pabusive = sum(train_category) / float(train_docs)  # 文档属于侮辱类的概率
    # p0num = np.zeros(words_cnt);
    # p1num = np.zeros(words_cnt)  # 创建numpy.zeros数组,词条出现数初始化为0
    # p0denom = 0.0
    # p1denom = 0.0
    # 分类器改进，
    p0num = np.ones(words_cnt);
    p1num = np.ones(words_cnt)  # 创建numpy.ones数组,词条出现数初始化为1
    p0denom = 2.0
    p1denom = 2.0
    for i in range(train_docs):
        if train_category[i] == 1:  #统计属于侮辱类的条件概率所需的数据，即P(w0|1),P(w1|1),P(w2|1)···
            p1num += train_matrix[i]
            p1denom += sum(train_matrix[i])
        else:  #统计属于非侮辱类的条件概率所需的数据，即P(w0|0),P(w1|0),P(w2|0)···
            p0num += train_matrix[i]
            p0denom += sum(train_matrix[i])
    # p0vect = p0num / p0denom
    # p1vect = p1num / p1denom
    p0vect = np.log(p0num / p0denom)
    p1vect = np.log(p1num / p1denom)
    return p0vect, p1vect, pabusive

"""
p0vect：每篇文章侮辱性词汇出现概率
p1vect：每篇文章非侮辱性词汇出现概率
pclass：样本（多篇文章）出现侮辱性词汇文章的概率？
"""
def classify_nb(vec_classify, p0vect, p1vect, pclass):
    ## 因为p0vect，p1vect都是取自然对数：logab = loga + logb，所以 pclass 需要取对数
    p0 = sum(vec_classify * p0vect) + np.log(pclass)
    p1 = sum(vec_classify * p1vect) + np.log(1.0 - pclass)
    if p0 < p1 :
        return 1
    else:
        return 0

"""
文档词袋模型
"""
def bag_of_words_vec(vocab_list, input_set):
    return_vec = [0] * len(vocab_list)
    for word in input_set :
        if word in vocab_list :
            return_vec[vocab_list.index(word)] += 1
        else :
            print("the word: %s is not in my Vocabulary!" % word)
    return return_vec

"""
接收一个大字符串并将其解析为字符串列表
"""
def text_parse(big_text) :
    import re
    # 将特殊符号作为切分标志进行字符串切分，即非字母、非数字
    list_tokens = re.split(r'\W+',big_text)
    # 除了单个字母，例如大写的I，其它单词变成小写
    return [tok.lower() for tok in list_tokens if len(tok) > 2]

def text_parse_test(big_text) :
    import re
    #reg = re.compile('[\\W]*')  # 我们可以使用正则表达式来切分句子，切分的规则是除单词，数字外的任意字符串
    #list_tokens = reg.split(big_text)

    # 将特殊符号作为切分标志进行字符串切分，即非字母、非数字
    list_tokens = re.split(r'\W+',big_text)
    # 除了单个字母，例如大写的I，其它单词变成小写
    return [tok.lower() for tok in list_tokens if len(tok) > 2]


"""
计算高频词汇
"""
def calc_most_freq(vocab_list, full_text) :
    freq_dict = {}
    for token in vocab_list :
        freq_dict[token] = full_text.count(token)
    sorted_freq = sorted(freq_dict.items(),key=operator.itemgetter(1), reverse=True)
    return sorted_freq[:30]

def local_words(feed1,feed0) :
    doc_list = []
    class_list = []
    full_text = []
    # 取最小长度
    min_len = min(len(feed1['entries']),len(feed0['entries']))
    for i in range(min_len):
        word_list = text_parse(feed1['entries'][i]['title'])
        doc_list.append(word_list)
        full_text.extend(word_list)
        class_list.append(1)
        word_list = text_parse(feed0['entries'][i]['title'])
        doc_list.append(word_list)
        full_text.extend(word_list)
        class_list.append(0)

    vocab_list = create_vocab_list(doc_list)
    top_thirty_words = calc_most_freq(vocab_list, full_text)
    for pairw in top_thirty_words :
        if pairw[0] in vocab_list :
            vocab_list.remove(pairw[0])
    training_set = list(range(2 * min_len))
    test_set = []
    for i in range(20) :
        rand_index = int(random.uniform(0, len(training_set)))
        test_set.append(training_set[rand_index])
        del(training_set[rand_index])
    train_mat = []
    train_classes = []
    for doc_index in training_set:
        train_mat.append(bag_of_words_vec(vocab_list, doc_list[doc_index]))
        train_classes.append(class_list[doc_index])
    p0V, p1V, pAb = train_nb0(train_mat, train_classes)
    error_count = 0
    for doc_index in test_set:
        word_vect = bag_of_words_vec(vocab_list, doc_list[doc_index])
        if classify_nb(word_vect, p0V, p1V, pAb) != class_list[doc_index]:
            error_count += 1
    print('the error rate is : {}'.format(float(error_count) / len(test_set)))
    return vocab_list,p0V,p1V

def get_top_words(ny,sf) :
    vocab_list,p0v,p1v = local_words(ny,sf)
    top_ny = []
    top_sf = []
    for i in range(len(p0v)) :
        if p0v[i] > -6.0 :
            top_sf.append((vocab_list[i],p0v[i]))
        if p1v[i] > -6.0 :
            top_ny.append((vocab_list[i],p1v[i]))
    # 按照元素的第二个排序
    #print(top_sf)
    sorted_sf = sorted(top_sf,key=lambda pair: pair[1],reverse=True)
    print("sf******************sf**********************sf\n", sorted_sf)
    sorted_ny = sorted(top_ny,key=lambda pair: pair[1],reverse=True)
    print("ny******************ny**********************ny\n", sorted_ny)

