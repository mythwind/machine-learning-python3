# !/usr/bin/python3


"""
面向对象技术简介
    类(Class): 用来描述具有相同的属性和方法的对象的集合。它定义了该集合中每个对象所共有的属性和方法。对象是类的实例。
    方法：类中定义的函数。
    类变量：类变量在整个实例化的对象中是公用的。类变量定义在类中且在函数体之外。类变量通常不作为实例变量使用。
    数据成员：类变量或者实例变量用于处理类及其实例对象的相关的数据。
    方法重写：如果从父类继承的方法不能满足子类的需求，可以对其进行改写，这个过程叫方法的覆盖（override），也称为方法的重写。
    局部变量：定义在方法中的变量，只作用于当前实例的类。
    实例变量：在类的声明中，属性是用变量来表示的，这种变量就称为实例变量，实例变量就是一个用 self 修饰的变量。
    继承：即一个派生类（derived class）继承基类（base class）的字段和方法。继承也允许把一个派生类的对象作为一个基类对象对待。例如，有这样一个设计：一个Dog类型的对象派生自Animal类，这是模拟"是一个（is-a）"关系（例图，Dog是一个Animal）。
    实例化：创建一个类的实例，类的具体对象。
    对象：通过类定义的数据结构实例。对象包括两个数据成员（类变量和实例变量）和方法。
    和其它编程语言相比，Python 在尽可能不增加新的语法和语义的情况下加入了类机制。

Python中的类提供了面向对象编程的所有基本功能：类的继承机制允许多个基类，派生类可以覆盖基类中的任何方法，方法中可以调用基类中的同名方法。

"""

class MyClass:
    """一个简单的类实例"""
    i = 12345
    def f(self):
        return 'hello world'

class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart

class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart

class Test:
    def prt1(self):
        print(self)
        print(self.__class__)
    def prt2(args):
        print(args)
        print(args.__class__)

#类定义
class people:
    #定义基本属性
    name = ''
    age = 0
    #定义私有属性,私有属性在类外部无法直接进行访问
    __weight = 0
    #定义构造方法
    def __init__(self,n,a,w):
        self.name = n
        self.age = a
        self.__weight = w
    def speak(self):
        print("%s 说: 我 %d 岁。" %(self.name,self.age))

# 单继承示例
class student(people):
    grade = ''
    def __init__(self, n, a, w, g):
        # 调用父类的构函
        people.__init__(self, n, a, w)
        self.grade = g

    # 覆写父类的方法
    def speak(self):
        print("%s 说: 我 %d 岁了，我在读 %d 年级" % (self.name, self.age, self.grade))

# 另一个类，多重继承之前的准备
class speaker():
    topic = ''
    name = ''
    def __init__(self, n, t):
        self.name = n
        self.topic = t

    def speak(self):
        print("我叫 %s，我是一个演说家，我演讲的主题是 %s" % (self.name, self.topic))

# 多重继承
class sample(speaker, student):
    a = ''
    def __init__(self, n, a, w, g, t):
        student.__init__(self, n, a, w, g)
        speaker.__init__(self, n, t)


class Parent:  # 定义父类
    def myMethod(self):
        print('调用父类方法')


class Child(Parent):  # 定义子类
    def myMethod(self):
        print('调用子类方法')



def test_01() :
    # 实例化类
    x = MyClass()
    # 访问类的属性和方法
    print("MyClass 类的属性 i 为：", x.i)
    print("MyClass 类的方法 f 输出为：", x.f())

    x = Complex(3.0, -4.5)
    print(x.r, x.i)  # 输出结果：3.0 -4.5

    t = Test()
    t.prt1()
    t.prt2()

def test_02_inherit() :
    # 实例化类
    p = people('runoob', 10, 30)
    p.speak()

    s = student('ken', 10, 60, 3)
    s.speak()

    test = sample("Tim", 25, 80, 4, "Python")
    test.speak()  # 方法名同，默认调用的是在括号中排前地父类的方法

    c = Child()  # 子类实例
    c.myMethod()  # 子类调用重写方法
    super(Child, c).myMethod()  # 用子类对象调用父类已被覆盖的方法


class JustCounter:
    __secretCount = 0  # 私有变量
    publicCount = 0  # 公开变量

    def count(self):
        self.__secretCount += 1
        self.publicCount += 1
        print(self.__secretCount)


class Site:
    def __init__(self, name, url):
        self.name = name  # public
        self.__url = url  # private

    def who(self):
        print('name  : ', self.name)
        print('url : ', self.__url)

    def __foo(self):  # 私有方法
        print('这是私有方法')

    def foo(self):            # 公共方法
        print('这是公共方法')
        self.__foo()


'''
类的私有属性
    __private_attrs：两个下划线开头，声明该属性为私有，不能在类的外部被使用或直接访问。在类内部的方法中使用时 self.__private_attrs。
类的方法
    在类的内部，使用 def 关键字来定义一个方法，与一般函数定义不同，类方法必须包含参数 self，且为第一个参数，self 代表的是类的实例。self 的名字并不是规定死的，也可以使用 this，但是最好还是按照约定是用 self。
类的私有方法
    __private_method：两个下划线开头，声明该方法为私有方法，只能在类的内部调用 ，不能在类的外部调用。self.__private_methods。
'''
def test_03_class_area() :
    counter = JustCounter()
    counter.count()
    counter.count()
    print(counter.publicCount)
    print(counter.__secretCount)  # 报错，实例不能访问私有变量

    x = Site('Python教程', 'www.mythwind.com')
    x.who()  # 正常输出
    x.foo()  # 正常输出
    x.__foo()  # 报错

"""
一般有三种命名空间：
    内置名称（built-in names）， Python 语言内置的名称，比如函数名 abs、char 和异常名称 BaseException、Exception 等等。
    全局名称（global names），模块中定义的名称，记录了模块的变量，包括函数、类、其它导入的模块、模块级的变量和常量。
    局部名称（local names），函数中定义的名称，记录了函数的变量，包括函数的参数和局部定义的变量。（类中定义的也是）
命名空间查找顺序:
    假设我们要使用变量 a，则 Python 的查找顺序为：局部的命名空间去 -> 全局命名空间 -> 内置命名空间。
    如果找不到变量 a，它将放弃查找并引发一个 NameError 异常:NameError: name 'runoob' is not defined。
命名空间的生命周期：
    命名空间的生命周期取决于对象的作用域，如果对象执行完成，则该命名空间的生命周期就结束。因此，我们无法从外部命名空间访问内部命名空间的对象。

作用域: 变量的作用域决定了在哪一部分程序可以访问哪个特定的变量名称。Python的作用域一共有4种，分别是：
    L（Local）：最内层，包含局部变量，比如一个函数/方法内部。
    E（Enclosing）：包含了非局部(non-local)也非全局(non-global)的变量。比如两个嵌套函数，一个函数（或类） A 里面又包含了一个函数 B ，那么对于 B 中的名称来说 A 中的作用域就为 nonlocal。
    G（Global）：当前脚本的最外层，比如当前模块的全局变量。
    B（Built-in）： 包含了内建的变量/关键字等。，最后被搜索
    规则顺序： L –> E –> G –> B。在局部找不到，便会去局部外的局部找（例如闭包），再找不到就会去全局找，再者去内置中找。
    


"""
def test_04_namespace() :
    fun1()
    print(num)
    outer()

num = 1
'''
当内部作用域想修改外部作用域的变量时，就要用到global和nonlocal关键字了。
'''
def fun1() :
    global num     # 需要使用 global 关键字声明
    print("函数 fun1 内部：",num)
    num = 123
    print("函数 fun1 内部：",num)

'''
如果要修改嵌套作用域（enclosing 作用域，外层非全局作用域）中的变量则需要 nonlocal 关键字了
'''
def outer():
    num = 10
    def inner():
        nonlocal num   # nonlocal关键字声明
        num = 100
        print(num)
    inner()
    print(num)

if __name__ == '__main__' :
    #test_01()
    #test_02_inherit()
    #test_03_class_area()
    test_04_namespace()
