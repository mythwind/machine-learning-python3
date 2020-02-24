
import bayes.prime_bayes as prime_bayes
import machine.constants as consts
import os
import random
import feedparser


def bayes() :
    posting_list = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],    ## stupid
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    class_vec = [0,1,0,1,0,1]   #根据样本内容判断是否包含侮辱性词汇

    print('postingList:\n', posting_list)
    vocab_list = prime_bayes.create_vocab_list(posting_list)
    print('vocab_list:\n', vocab_list)

    trainMat = []
    for doc in posting_list:
        trainMat.append(prime_bayes.setofwords_vec(vocab_list, doc))
    print('trainMat:\n', trainMat)
    p0V, p1V, pAb = prime_bayes.train_nb0(trainMat, class_vec)
    test_entry = ['love', 'my', 'dalmation']
    test_doc = prime_bayes.setofwords_vec(vocab_list, test_entry)
    if prime_bayes.classify_nb(test_doc,p0V,p1V,pAb) :
        print(test_entry, '属于侮辱类')  # 执行分类并打印分类结果
    else:
        print(test_entry, '属于非侮辱类')
    test_entry = ['stupid', 'garbage']
    test_doc = prime_bayes.setofwords_vec(vocab_list, test_entry)
    print('test_doc:\n', test_doc)
    print("\np0v:{}\np1v:{}\npAb:{}".format(p0V,p1V,pAb))
    if prime_bayes.classify_nb(test_doc, p0V, p1V, pAb):
        print(test_entry, '属于侮辱类')  # 执行分类并打印分类结果
    else:
        print(test_entry, '属于非侮辱类')

def email_spam() :
    doc_list = []
    class_list = []
    full_text = []
    listx = os.listdir(consts.DIR_BAYES_SPAN_PATH)  # 列出文件夹下所有的目录与文件
    for i in range(1, len(listx) + 1) :
        word_list = prime_bayes.text_parse(open(consts.DIR_BAYES_SPAN_PATH + '/%d.txt'%i,encoding='ISO-8859-1').read())
        doc_list.append(word_list)
        full_text.extend(word_list)
        class_list.append(1)
        word_list = prime_bayes.text_parse(open(consts.DIR_BAYES_HAM_PATH + '/%d.txt' % i,encoding='ISO-8859-1').read())
        doc_list.append(word_list)
        full_text.extend(word_list)
        class_list.append(0)

    vocab_list = prime_bayes.create_vocab_list(doc_list)
    training_set = list(range(50))
    test_set = []
    for i in range(10) :
        rand_index = int(random.uniform(0, len(training_set)))
        test_set.append(training_set[rand_index])
        del(training_set[rand_index])
    train_mat = []
    train_classes = []
    for doc_index in training_set :
        train_mat.append(prime_bayes.setofwords_vec(vocab_list, doc_list[doc_index]))
        train_classes.append(class_list[doc_index])
    p0V, p1V, pAb = prime_bayes.train_nb0(train_mat, train_classes)
    error_count = 0
    for doc_index in test_set :
        word_vect = prime_bayes.setofwords_vec(vocab_list, doc_list[doc_index])
        if prime_bayes.classify_nb(word_vect, p0V, p1V, pAb) != class_list[doc_index] :
            error_count += 1
    print('the error rate is : {}'.format(float(error_count) / len(test_set)))

def rss_test() :
    # ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
    # sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
    ny = feedparser.parse('feed://www.chinadaily.com.cn/rss/china_rss.xml')
    sf = feedparser.parse('feed://www.chinadaily.com.cn/rss/world_rss.xml')
    print(ny)
    print(sf)
    #prime_bayes.local_words(ny,sf)
    prime_bayes.get_top_words(ny,sf)

if __name__ == '__main__' :
    # machine()
    # bayes()
    # email_spam()
    rss_test()

