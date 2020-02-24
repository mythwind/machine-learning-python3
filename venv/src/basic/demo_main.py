#!/usr/bin/python3

import sys
import keyword
import pickle
import pprint
import os.path
import shutil
import glob
import re
import math
import random
import datetime
import zlib

import constants

### 定义常量的方法
constants.PI = 3.14
constants.FILE_PATH_FOO = "assets/foo.txt"
constants.FILE_PATH_PICKLE = "assets/data.pkl"



"""
key：关键字，注释，打印
多行注释可以三个单引号，也可以三个双引号
"""
def test_01_basice() :
    print("Python 一定要注意缩进，缩进不一致，会导致运行错误！")
    print(keyword.kwlist)   #单行注释，打印关键字
    # 多行需要用反斜杠(\)拼接
    item_one = 1
    item_two = 2
    item_three = 3
    total = item_one + \
        item_two + \
        item_three
    print("%d + %d + %d = %d"%(item_one,item_two,item_three,total))
    ###同一行显示多条语句
    import sys;x = 'runoob';sys.stdout.write(x + '\n')
    print("在 python 用 import 或者 from...import 来导入相应的模块。\n"
          + "\t将整个模块(somemodule)导入，格式为： import somemodule。\n"
          + "\t从某个模块中导入某个函数,格式为： from somemodule import somefunction。\n"
          + "\t从某个模块中导入多个函数,格式为： from somemodule import firstfunc, secondfunc, thirdfunc。\n"
          + "\t将某个模块中的全部函数导入，格式为： from somemodule import * 。\n")

"""
字符串：
    用单引号 ' 或双引号 " 括起来，同时使用反斜杠 \ 转义特殊字符。
    1、反斜杠可以用来转义，使用r可以让反斜杠不发生转义。
    2、字符串可以用+运算符连接在一起，用*运算符重复。
    3、Python中的字符串有两种索引方式，从左往右以0开始，从右往左以-1开始。
    4、Python中的字符串不能改变。
    x=1
    print(f'{x+1}')   # Python 3.6  新增 f-string
    print(f'{x+1=}')   # Python 3.8  新增=拼接
    
"""
def test_02_string() :
    str = "Python Learning"
    print('string------------------------------')
    print(str)  # 输出字符串
    print(str[0:-1])  # 输出第一个到倒数第二个的所有字符
    print(str[0])  # 输出字符串第一个字符
    print(str[2:5])  # 输出从第三个开始到第五个的字符
    print(str[2:])  # 输出从第三个开始后的所有字符
    print(str * 2)  # 输出字符串两次
    print(str + '你好')  # 连接字符串
    print('hello\nRunoob')  # 使用反斜杠(\)+n转义特殊字符
    print(r'hello\nRunoob')  # 在字符串前面添加一个 r，表示原始字符串，不会发生转义
    # 不换行输出
    print("不换行输出%s! \t"%(str), end=" ")
    print("我是第二行！")
    word = 'Python'
    print(word[0], word[5])
    print(word[-1], word[-6])

    counter = 100  # 整型变量
    miles = 1000.0  # 浮点型变量
    a = b = c = 1
    a, b, c, d = 20, 5.5, True, 4+3j
    print(type(a), type(b), type(c), type(d))
    print('string end------------------------------')

"""
列表：
    可以完成大多数集合类的数据结构实现。列表中元素的类型可以不相同，它支持数字，字符串甚至可以包含列表（所谓嵌套）。
    列表是写在方括号 [] 之间、用逗号分隔开的元素列表。列表中的元素是可以改变的。
    和字符串一样，列表同样可以被索引和截取，列表被截取后返回一个包含所需元素的新列表。
    1、List写在方括号之间，元素用逗号隔开。
    2、和字符串一样，list可以被索引和切片。
    3、List可以使用+操作符进行拼接。
    4、List中的元素是可以改变的。
"""
def test_03_list() :
    print('list------------------------------')
    list = ['abcd', 786, 2.23, 'runoob', 70.2]
    tinylist = [123, 'runoob']
    print(list)  # 输出完整列表
    print(list[0])  # 输出列表第一个元素
    print(list[1:3])  # 从第二个开始输出到第三个元素
    print(list[2:])  # 输出从第三个元素开始的所有元素
    #加号 + 是列表连接运算符，星号 * 是重复操作。
    print(tinylist * 2)  # 输出两次列表
    print(list + tinylist)  # 连接列表
    ## 改变列表元素
    a = [1, 2, 3, 4, 5, 6]
    a[0] = 9
    print(a)
    a[2:5] = [13, 14, 15]
    print(a)
    ## 字符串逆向
    str = "I Love You"
    inputwords = str.split(" ")
    # 第一个参数 -1 表示最后一个元素
    # 第二个参数为空，表示移动到列表末尾
    # 第三个参数为步长，-1 表示逆向
    inputwords = inputwords[-1::-1]
    print(' '.join(inputwords))
    print('list end------------------------------')

"""
元组：
    元组（tuple）与列表类似，不同之处在于元组的元素不能修改。元组写在小括号 () 里，元素之间用逗号隔开。
    其实，可以把字符串看作一种特殊的元组。
    1、与字符串一样，元组的元素不能修改。
    2、元组也可以被索引和切片，方法一样。
    3、注意构造包含 0 或 1 个元素的元组的特殊语法规则。
    4、元组也可以使用+操作符进行拼接
"""
def test_04_tuple() :
    print('tuple------------------------------')
    tuple = ('abcd', 786, 2.23, 'runoob', 70.2)
    tinytuple = (123, 'runoob')
    print(tuple)  # 输出完整元组
    print(tuple[0])  # 输出元组的第一个元素
    print(tuple[1:3])  # 输出从第二个元素开始到第三个元素
    print(tuple[2:])  # 输出从第三个元素开始的所有元素
    print(tinytuple * 2)  # 输出两次元组
    print(tuple + tinytuple)  # 连接元组
    print('tuple end------------------------------')

"""
集合（set）是由一个或数个形态各异的大小整体组成的，构成集合的事物或对象称作元素或是成员。
可以使用大括号 { } 或者 set() 函数创建集合，注意：创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典。
"""
def test_05_set() :
    print('set------------------------------')
    student = {'Tom', 'Jim', 'Mary', 'Tom', 'Jack', 'Rose'}
    print(student)  # 输出集合，重复的元素被自动去掉
    # 成员测试
    if 'Rose' in student:
        print('Rose 在集合中')
    else:
        print('Rose 不在集合中')
    # set可以进行集合运算
    a = set('abracadabra')
    b = set('alacazam')
    print(a)
    print(a - b)  # a 和 b 的差集
    print(a | b)  # a 和 b 的并集
    print(a & b)  # a 和 b 的交集
    print(a ^ b)  # a 和 b 中不同时存在的元素
    print('set end------------------------------')

def square(x) :            # 计算平方数
    return x ** 2

"""
map() 会根据提供的函数对指定序列做映射。
第一个参数 function 以参数序列中的每一个元素调用 function 函数，返回包含每次 function 函数返回值的新列表
"""
def test_05_map():
    x = map(square, [1, 2, 3, 4, 5])  # 计算列表各个元素的平方
    print(list(x))
    y = map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10])
    print(list(y))

"""
字典（dictionary）:
    列表是有序的对象集合，字典是无序的对象集合。两者之间的区别在于：字典当中的元素是通过键来存取的，而不是通过偏移存取。
    字典是一种映射类型，字典用 { } 标识，它是一个无序的 键(key) : 值(value) 的集合。
    键(key)必须使用不可变类型。
    在同一个字典中，键(key)必须是唯一的。
    1、字典是一种映射类型，它的元素是键值对。
    2、字典的关键字必须为不可变类型，且不能重复。
    3、创建空字典使用 { }。
"""
def test_06_dictionary() :
    dictx = {}
    dictx['one'] = "1 - Python教程"
    dictx[2] = "2 - Python工具"
    tinydict = {'name': 'runoob', 'code': 1, 'site': 'www.runoob.com'}
    print(dictx['one'])  # 输出键为 'one' 的值
    print(dictx[2])  # 输出键为 2 的值
    del dictx['one']  # 删除键 'one'
    print(dict)
    dictx.clear()  # 清空字典
    del dictx  # 删除字典
    print(tinydict)  # 输出完整的字典
    print(tinydict.keys())  # 输出所有键
    print(tinydict.values())  # 输出所有值

    dict1 = dict([('Runoob', 1), ('Google', 2), ('Taobao', 3)])
    dict2 = {x: x ** 2 for x in (2, 4, 6)}
    dict3 = dict(Runoob=1, Google=2, Taobao=3)
    print(dict1,dict2,dict3)


def test_07_fibonacci() :
    a,b= 0,1
    while b < 10 :
        print(b,end=",")
        a,b=b,a+b
    sum = a + b
    print()
    print(sum)

def test_gene_fibonacci(n):
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a
        a, b = b, a + b
        counter += 1

def test_08_iter() :
    mclass = MyNumbers1()
    miter = iter(mclass)
    for x in miter:
        print("my class number iter:%d" % (x))

    list = [1, 2, 3, 4]
    it = iter(list)  # 创建迭代器对象
    for x in it:
        print(x, end=" ")
    print("--------------------")
    it = iter(list)  # 创建迭代器对象
    while True:
        try:
            print(next(it))
        except StopIteration:
            sys.exit()


class MyNumbers1 :
    def __iter__(self):
        self.a = 1 
        return self

    def __next__(self):
        if self.a  <= 20 :
            x = self.a
            self.a += 1
            return x
        else :
            raise StopIteration

"""
加了星号 * 的参数会以元组(tuple)的形式导入，存放所有未命名的变量参数。
"""
def test_09_func_tuple(arg1, *vartuple) :
    "打印任何传入的参数"
    print("参数可变函数 tuple，输出: ")
    print(arg1)
    print(vartuple)

"""
加了两个星号 ** 的参数会以字典的形式导入。
"""
def test_09_func_dict(arg1, **vardict ) :
    print("输出: ")
    print(arg1)
    print(vardict)

"""
如果单独出现星号 * 后的参数必须用关键字传入。
"""
def test_09_func_star(a,b,*,c):
    return a + b + c

"""
匿名函数：使用 lambda 来创建匿名函数。所谓匿名，意即不再使用 def 语句这样标准的形式定义一个函数。
    lambda 只是一个表达式，函数体比 def 简单很多。
    lambda的主体是一个表达式，而不是一个代码块。仅仅能在lambda表达式中封装有限的逻辑进去。
    lambda 函数拥有自己的命名空间，且不能访问自己参数列表之外或全局命名空间里的参数。
    虽然lambda函数看起来只能写一行，却不等同于C或C++的内联函数，后者的目的是调用小函数时不占用栈内存从而增加运行效率。
"""
def test_09_func_noname() :
    # 可写函数说明
    sum = lambda arg1, arg2: arg1 + arg2
    # 调用sum函数
    print("相加后的值为 : ", sum(10, 20))
    print("相加后的值为 : ", sum(20, 20))

"""
定义一个函数，以下是简单的规则：
    函数代码块以 def 关键词开头，后接函数标识符名称和圆括号 ()。
    任何传入参数和自变量必须放在圆括号中间，圆括号之间可以用于定义参数。
    函数的第一行语句可以选择性地使用文档字符串—用于存放函数说明。
    函数内容以冒号起始，并且缩进。
    return [表达式] 结束函数，选择性地返回一个值给调用方。不带表达式的return相当于返回 None。
参数传递:可更改(mutable)与不可更改(immutable)对象
    在 python 中，strings, tuples, 和 numbers 是不可更改的对象，而 list,dict 等则是可以修改的对象。
    不可变类型：变量赋值 a=5 后再赋值 a=10，这里实际是新生成一个 int 值对象 10，再让 a 指向它，而 5 被丢弃，不是改变a的值，相当于新生成了a。
    可变类型：变量赋值 la=[1,2,3,4] 后再赋值 la[2]=5 则是将 list la 的第三个元素值更改，本身la没有动，只是其内部的一部分值被修改了。
python 函数的参数传递：
    不可变类型：类似 c++ 的值传递，如 整数、字符串、元组。如fun（a），传递的只是a的值，没有影响a对象本身。比如在 fun（a）内部修改 a 的值，只是修改另一个复制的对象，不会影响 a 本身。
    可变类型：类似 c++ 的引用传递，如 列表，字典。如 fun（la），则是将 la 真正的传过去，修改后fun外部的la也会受影响
"""
def test_09_func():
    test_09_func_tuple( 70, 60, 50)
    test_09_func_dict(70, a=60, b=50)
    #test_09_func_star(70,50,20)   # error
    test_09_func_star(70,50,c=20)

"""
import 语句
    当解释器遇到 import 语句，如果模块在当前的搜索路径就会被导入。
    搜索路径是一个解释器会先进行搜索的所有目录的列表。
    一个模块只会被导入一次，不管你执行了多少次import。
from … import 语句
    Python 的 from 语句让你从模块中导入一个指定的部分到当前命名空间中
dir() 函数
    内置的函数 dir() 可以找到模块内定义的所有名称
package
    包是一种管理 Python 模块命名空间的形式，采用"点模块名称"。
"""
def test_10_moduels():
    pass

"""
输出格式美化
repr() 函数可以转义字符串中的特殊字符

"""
def test_11_io():
    s = 'Hello, Runoob'
    print(str(s))
    print(repr(s))
    hello = 'hello, runoob\n'
    print(repr(hello))
    for x in range(1, 11):
        print(repr(x).rjust(2), repr(x * x).rjust(3), end=' ')
        print(repr(x * x * x).rjust(4))
    print("==================")
    for x in range(1, 11):
        print('{0:2d} {1:3d} {2:4d}'.format(x, x * x, x * x * x))
    print('{}网址： "{}!"'.format('Python教程', 'www.mythwind.com'))
    print('{0} 和 {1}'.format('Google', 'Runoob'))
    table = {'Google': 1, 'Runoob': 2, 'Taobao': 3}
    print('Runoob: {0[Runoob]:d}; Google: {0[Google]:d}; Taobao: {0[Taobao]:d}'.format(table))
    print('Runoob: {Runoob:d}; Google: {Google:d}; Taobao: {Taobao:d}'.format(**table))
    str = input("请输入：");
    print("你输入的内容是: ", str)

def test_12_file() :
    print('Python %s on %s' % (sys.version, sys.platform))
    fr = open(constants.FILE_PATH_FOO)
    print("read file before write, content:",fr.read())
    fr.close()
    fr = open(constants.FILE_PATH_FOO, "a+", encoding='utf-8')
    fr.write("\nPython 是一个非常好的语言。\n是的，的确非常好!!")
    fr.close()
    fr = open(constants.FILE_PATH_FOO)
    print("read file after write, content:", fr.read())
    fr.close()

"""
python的pickle模块实现了基本的数据序列和反序列化。
    通过pickle模块的序列化操作我们能够将程序中运行的对象信息保存到文件中去，永久存储。
    通过pickle模块的反序列化操作，我们能够从文件中创建上一次程序保存的对象。
"""
def test_13_pickle():
    # 使用pickle模块将数据对象保存到文件
    
    data1 = {'a': [1, 2.0, 3, 4 + 6j],
             'b': ('string', u'Unicode string'),
             'c': None}
    selfref_list = [1, 2, 3]
    selfref_list.append(selfref_list)
    output = open(constants.FILE_PATH_PICKLE, 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(data1, output)
    # Pickle the list using the highest protocol available.
    pickle.dump(selfref_list, output, -1)
    output.close()

    # 使用pickle模块从文件中重构python对象
    pkl_file = open(constants.FILE_PATH_PICKLE, 'rb')
    data1 = pickle.load(pkl_file)
    pprint.pprint(data1)
    data2 = pickle.load(pkl_file)
    pprint.pprint(data2)
    pkl_file.close()

def test_14_os() :
    print(os.path.abspath(""))  # 查看当前绝对路径
    print(os.getcwd())          # 返回一个当前工作目录的Unicode对象

"""
异常处理
try/except
异常捕捉可以使用 try/except 语句。
    首先，执行 try 子句（在关键字 try 和关键字 except 之间的语句）。
    如果没有异常发生，忽略 except 子句，try 子句执行后结束。
    如果在执行 try 子句的过程中发生了异常，那么 try 子句余下的部分将被忽略。如果异常的类型和 except 之后的名称相符，那么对应的 except 子句将被执行。
    如果一个异常没有与任何的 excep 匹配，那么这个异常将会传递给上层的 try 中。
    
try/except...else
try/except 语句还有一个可选的 else 子句，如果使用这个子句，那么必须放在所有的 except 子句之后。
else 子句将在 try 子句没有发生任何异常的时候执行。

try-finally 语句
try-finally 语句无论是否发生异常都将执行最后的代码。

Python 使用 raise 语句抛出一个指定的异常。
"""
def test_15_exception() :
    while True:
        try:
            x = int(input("请输入一个数字: "))
            break
        except ValueError:
            print("您输入的不是数字，请再次尝试输入！")

def test_16_std() :
    print(os.getcwd())     # 返回当前的工作目录
    #shutil.copyfile('data.db', 'archive.db')   #针对日常的文件和目录管理任务,shutil
    glob.glob('*.py')       #glob模块提供了一个函数用于从目录通配符搜索中生成文件列表
    print(sys.argv)         #命令行参数
    sys.stderr.write('Warning, log file not found starting a new one\n') #错误输出重定向和程序终止
    str1 = re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest')
    print(str1)
    str1 = re.sub(r'(\b[a-z]+) \1', r'\1', 'cat in the the hat')
    print(str1)
    print(math.cos(math.pi / 4))
    print(math.log(1024, 2))
    print(random.choice(['apple', 'pear', 'banana']))
    print(datetime.date.today())  #日期和时间
    print(datetime.date(1964, 7, 31))
    ## 压缩
    s = b'witch which has which witches wrist watch'
    print(len(s))
    t = zlib.compress(s)
    print(len(t))
    print(zlib.decompress(t))
    print(zlib.crc32(s))


if __name__ == '__main__' :
    #test_01_basice()
    # string、list 和 tuple 都属于 sequence（序列）。
    #test_02_string()
    #test_03_list()
    #test_04_tuple()
    #test_05_set()
    #test_05_map()
    #test_06_dictionary()
    #test_07_fibonacci()
    #test_gene_fibonacci()
    #test_08_iter()
    #test_09_func()
    #test_10_moduels()
    #test_11_io()
    #test_12_file()
    #test_13_pickle()
    #test_14_os()
    #test_15_exception()
    test_16_std()
    print("===END===")

