#!/usr/bin/python

import time
import re
import mysql.connector
import pymysql
import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
import numpy as np
import matplotlib.pyplot as plt

#import _thread
import threading
#import constants_new
from constants_new import _mconstants
import xml.sax
from xml.dom.minidom import parse
import xml.dom.minidom
import json


constants = _mconstants()

"""
正则表达式修饰符 - 可选标志
正则表达式可以包含一些可选标志修饰符来控制匹配的模式。修饰符被指定为一个可选的标志。多个标志可以通过按位 OR(|) 它们来指定。如 re.I | re.M 被设置成 I 和 M 标志：
    re.I	使匹配对大小写不敏感
    re.L	做本地化识别（locale-aware）匹配
    re.M	多行匹配，影响 ^ 和 $
    re.S	使 . 匹配包括换行在内的所有字符
    re.U	根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.
    re.X	该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。


re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None；
而re.search匹配整个字符串，直到找到一个匹配。

findall
    在字符串中找到正则表达式所匹配的所有子串，并返回一个列表，如果没有找到匹配的，则返回空列表。
    注意： match 和 search 是匹配一次 findall 匹配所有。

"""
def test_01_regular() :
    print(re.match('www', 'www.mythwind.com').span())  # 在起始位置匹配
    print(re.match('com', 'www.mythwind.com'))  # 不在起始位置匹配
    print(re.match('1234', 'www.mythwind.com'))

    line = "Cats are smarter than dogs"
    # .* 表示任意匹配除换行符（\n、\r）之外的任何单个或多个字符
    matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)
    print("matchObj.group() : ", matchObj.group())
    print("matchObj.group(2) : ", matchObj.group(2))
    searchObj = re.search(r'(.*) are (.*?) .*', line, re.M | re.I)
    print("searchObj.group() : ", searchObj.group())
    print("searchObj.group(2) : ", searchObj.group(2))

    matchObj = re.match(r'dogs', line, re.M | re.I)
    if matchObj:
        print("match --> matchObj.group() : ", matchObj.group())
    else:
        print("No match!!")

    matchObj = re.search(r'dogs', line, re.M | re.I)
    if matchObj:
        print("search --> matchObj.group() : ", matchObj.group())
    else:
        print("No match!!")

    phone = "2004-959-559 # 这是一个电话号码"
    # 删除注释
    num = re.sub(r'#.*$', "", phone)
    print("电话号码 : ", num)
    # 移除非数字的内容
    num = re.sub(r'\D', "", phone)
    print("电话号码 : ", num)

    pattern = re.compile(r'\d+')  # 查找数字
    result1 = pattern.findall('runoob 123 google 456')
    result2 = pattern.findall('run88oob123google456', 0, 10)
    print(result1)
    print(result2)

"""
CGI(Common Gateway Interface),通用网关接口,它是一段程序,运行在服务器上如：HTTP服务器，提供同客户端HTML页面的接口。
"""
def test_02_cgi() :
    pass

"""
安装数据库驱动mysql-connector-python
python -m pip install mysql-connector
"""
def test_03_mysql() :
    #10.211.55.3
    mydb = mysql.connector.connect(
        host="10.211.55.3",
        user="root",
        passwd="123456",
        database="mysql"
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE sites (name VARCHAR(255), url VARCHAR(255))")
    mycursor.execute("ALTER TABLE sites ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
    #mycursor.execute("CREATE TABLE sites (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), url VARCHAR(255))")
    #插入数据
    sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
    val = ("RUNOOB", "https://www.mythwind.com")
    mycursor.execute(sql, val)
    print("1 条记录已插入, ID:", mycursor.lastrowid)

    sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
    val = [
        ('Google', 'https://www.google.com'),
        ('Github', 'https://www.github.com'),
        ('Taobao', 'https://www.taobao.com'),
        ('stackoverflow', 'https://www.stackoverflow.com/')
    ]
    mycursor.executemany(sql, val)
    mydb.commit()  # 数据表内容有更新，必须使用到该语句
    print(mycursor.rowcount, "记录插入成功。")

    #查询数据
    mycursor.execute("SELECT * FROM sites")
    myresult = mycursor.fetchall()  # fetchall() 获取所有记录
    for x in myresult:
        print(x)

    #修改数据
    sql = "UPDATE sites SET name = %s WHERE name = %s"
    val = ("Zhihu", "ZH")
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, " 条记录被修改")

    #删除数据
    sql = "DELETE FROM sites WHERE name = %s"
    na = ("stackoverflow",)
    mycursor.execute(sql, na)
    mydb.commit()
    print(mycursor.rowcount, " 条记录删除")

def test_04_pymysql() :
    # 打开数据库连接
    db = pymysql.connect("10.211.55.3", "root", "123456", "mysql")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
    # 使用预处理语句创建表
    sql = """CREATE TABLE EMPLOYEE (
             FIRST_NAME  CHAR(20) NOT NULL,
             LAST_NAME  CHAR(20),
             AGE INT,  
             SEX CHAR(1),
             INCOME FLOAT )"""
    cursor.execute(sql)

    # SQL 插入语句
    sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
           LAST_NAME, AGE, SEX, INCOME) \
           VALUES ('%s', '%s',  %s,  '%s',  %s)" % \
          ('Mac', 'Mohan', 20, 'M', 2000)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    # SQL 查询语句
    sql = "SELECT * FROM EMPLOYEE \
           WHERE INCOME > %s" % (1000)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print(results)
        # for row in results:
        #     fname = row[0]
        #     lname = row[1]
        #     age = row[2]
        #     sex = row[3]
        #     income = row[4]
        #     # 打印结果
        #     print("fname=%s,lname=%s,age=%s,sex=%s,income=%s" % \
        #           (fname, lname, age, sex, income))
    except:
        print("Error: unable to fetch data")

    # SQL 更新语句
    sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    # SQL 删除语句
    sql = "DELETE FROM EMPLOYEE WHERE AGE > %s" % (20)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    db.close()

"""
Python 提供了两个级别访问的网络服务：
    低级别的网络服务支持基本的 Socket，它提供了标准的 BSD Sockets API，可以访问底层操作系统Socket接口的全部方法。
    高级别的网络服务模块 SocketServer， 它提供了服务器中心类，可以简化网络服务器的开发。
什么是 Socket?
    Socket又称"套接字"，应用程序通常通过"套接字"向网络发出请求或者应答网络请求，使主机间或者一台计算机上的进程间可以通讯。
"""
def network_server() :
    # 创建 socket 对象
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名
    host = socket.gethostname()
    port = 9999
    # 绑定端口号
    serversocket.bind((host, port))
    # 设置最大连接数，超过后排队
    serversocket.listen(5)
    while True:
        # 建立客户端连接
        clientsocket, addr = serversocket.accept()
        print("连接地址: %s" % str(addr))
        msg = '欢迎访问Python教程！' + "\r\n"
        clientsocket.send(msg.encode('utf-8'))
        clientsocket.close()

def network_client() :
    # 创建 socket 对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名
    host = socket.gethostname()
    # 设置端口号
    port = 9999
    # 连接服务，指定主机和端口
    s.connect((host, port))
    # 接收小于 1024 字节的数据
    msg = s.recv(1024)
    s.close()
    print(msg.decode('utf-8'))

def test_05_network() :
    network_server()
    network_client()

"""
SMTP（Simple Mail Transfer Protocol）即简单邮件传输协议,它是一组用于由源地址到目的地址传送邮件的规则，由它来控制信件的中转方式。
Python创建 SMTP 对象语法如下：
    import smtplib
    smtpObj = smtplib.SMTP( [host [, port [, local_hostname]]] )
    参数说明：
        host: SMTP 服务器主机。 你可以指定主机的ip地址或者域名如:runoob.com，这个是可选参数。
        port: 如果你提供了 host 参数, 你需要指定 SMTP 服务使用的端口号，一般情况下SMTP端口号为25。
        local_hostname: 如果SMTP在你的本机上，你只需要指定服务器地址为 localhost 即可。
Python SMTP对象使用sendmail方法发送邮件，语法如下：
    SMTP.sendmail(from_addr, to_addrs, msg[, mail_options, rcpt_options]
    参数说明：
        from_addr: 邮件发送者地址。
        to_addrs: 字符串列表，邮件发送地址。
        msg: 发送消息
    这里要注意一下第三个参数，msg是字符串，表示邮件。我们知道邮件一般由标题，发信人，收件人，邮件内容，附件等构成，发送邮件的时候，要注意msg的格式。这个格式就是smtp协议中定义的格式。
"""
def test_06_smtp() :
    sender = 'star2008wang@163.com'
    receivers = ['774202013@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
    message['From'] = Header("Pyth教程", 'utf-8')  # 发送者
    message['To'] = Header("测试", 'utf-8')  # 接收者

    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

    # 第三方 SMTP 服务
    mail_host = "smtp.XXX.com"  # 设置服务器
    mail_user = "XXXX"  # 用户名
    mail_pass = "XXXXXX"  # 口令
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("菜鸟教程", 'utf-8')
    message['To'] = Header("测试", 'utf-8')
    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText('这是菜鸟教程Python 邮件发送测试……', 'plain', 'utf-8'))

    # 构造附件1，传送当前目录下的 machine.txt 文件
    att1 = MIMEText(open('machine.txt', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="machine.txt"'
    message.attach(att1)

    # 构造附件2，传送当前目录下的 runoob.txt 文件
    att2 = MIMEText(open('runoob.txt', 'rb').read(), 'base64', 'utf-8')
    att2["Content-Type"] = 'application/octet-stream'
    att2["Content-Disposition"] = 'attachment; filename="runoob.txt"'
    message.attach(att2)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

    msgRoot = MIMEMultipart('related')
    msgRoot['From'] = Header("菜鸟教程", 'utf-8')
    msgRoot['To'] = Header("测试", 'utf-8')
    subject = 'Python SMTP 邮件测试'
    msgRoot['Subject'] = Header(subject, 'utf-8')

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    mail_msg = """
    <p>Python 邮件发送测试...</p>
    <p><a href="http://www.runoob.com">菜鸟教程链接</a></p>
    <p>图片演示：</p>
    <p><img src="cid:image1"></p>
    """
    msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    # 指定图片为当前目录
    fp = open('machine.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # 定义图片 ID，在 HTML 文本中引用
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, msgRoot.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

# 为线程定义一个函数
def print_time( threadName, delay):
   count = 0
   while count < 5:
        time.sleep(delay)
        count += 1
        print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

threadLock = threading.Lock()

class custom_thread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("开始线程：" + self.name)
        # 获取锁，用于线程同步
        threadLock.acquire()
        print_time2(self.name, self.counter, 5)
        # 释放锁，开启下一个线程
        threadLock.release()
        print ("退出线程：" + self.name)

def print_time2(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

"""
Python3 线程中常用的两个模块为：
    _thread
    threading(推荐使用)
thread 模块已被废弃。用户可以使用 threading 模块代替。所以，在 Python3 中不能再使用"thread" 模块。为了兼容性，Python3 将 thread 重命名为 "_thread"。

"""
def test_07_multi_thread():
    # 创建两个线程
    """
    try:
        _thread.start_new_thread(print_time, ("Thread-1", 2,))
        _thread.start_new_thread(print_time, ("Thread-2", 4,))
    except:
        print("Error: 无法启动线程")
    """

    threads = []

    # 创建新线程
    thread1 = custom_thread(1, "Thread-1", 1)
    thread2 = custom_thread(2, "Thread-2", 2)

    # 开启新线程
    thread1.start()
    thread2.start()

    # 添加线程到线程列表
    threads.append(thread1)
    threads.append(thread2)

    # 等待所有线程完成
    for t in threads:
        t.join()
    print("退出主线程")

def test_07_thread_queue() :

    pass


"""
Python 对 XML 的解析
常见的 XML 编程接口有 DOM 和 SAX，这两种接口处理 XML 文件的方式不同，当然使用场合也不同。
Python 有三种方法解析 XML，SAX，DOM，以及 ElementTree

SAX 是一种基于事件驱动的API。
利用 SAX 解析 XML 文档牵涉到两个部分: 解析器和事件处理器。
解析器负责读取 XML 文档，并向事件处理器发送事件，如元素开始跟元素结束事件。
而事件处理器则负责对事件作出响应，对传递的 XML 数据进行处理。
    1、对大型文件进行处理；
    2、只需要文件的部分内容，或者只需从文件中得到特定信息。
    3、想建立自己的对象模型的时候。
"""
def test_08_xml_sax() :
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # 关闭命名空间
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # 重写 ContextHandler
    handler = MovieHandler()
    parser.setContentHandler(handler)

    parser.parse(constants.FILE_XML_MOIVES)

class MovieHandler(xml.sax.ContentHandler) :
    def __init__(self):
        self.CurrentData = ""
        self.type = ""
        self.format = ""
        self.year = ""
        self.rating = ""
        self.stars = ""
        self.description = ""

        # 元素开始调用

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "movie":
            print("*****Movie*****")
            title = attributes["title"]
            print("Title:", title)

        # 元素结束调用

    def endElement(self, tag):
        if self.CurrentData == "type":
            print("Type:", self.type)
        elif self.CurrentData == "format":
            print("Format:", self.format)
        elif self.CurrentData == "year":
            print("Year:", self.year)
        elif self.CurrentData == "rating":
            print("Rating:", self.rating)
        elif self.CurrentData == "stars":
            print("Stars:", self.stars)
        elif self.CurrentData == "description":
            print("Description:", self.description)
        self.CurrentData = ""

        # 读取字符时调用

    def characters(self, content):
        if self.CurrentData == "type":
            self.type = content
        elif self.CurrentData == "format":
            self.format = content
        elif self.CurrentData == "year":
            self.year = content
        elif self.CurrentData == "rating":
            self.rating = content
        elif self.CurrentData == "stars":
            self.stars = content
        elif self.CurrentData == "description":
            self.description = content

"""
文件对象模型（Document Object Model，简称DOM），是W3C组织推荐的处理可扩展置标语言的标准编程接口。
一个 DOM 的解析器在解析一个 XML 文档时，一次性读取整个文档，把文档中所有元素保存在内存中的一个树结构里，之后你可以利用DOM 提供的不同的函数来读取或修改文档的内容和结构，也可以把修改过的内容写入xml文件。
"""
def test_09_xml_dom() :
    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse(constants.FILE_XML_MOIVES)
    collection = DOMTree.documentElement
    if collection.hasAttribute("shelf"):
        print("Root element : %s" % collection.getAttribute("shelf"))

    # 在集合中获取所有电影
    movies = collection.getElementsByTagName("movie")

    # 打印每部电影的详细信息
    for movie in movies:
        print("*****Movie*****")
        if movie.hasAttribute("title"):
            print("Title: %s" % movie.getAttribute("title"))

        type = movie.getElementsByTagName('type')[0]
        print("Type: %s" % type.childNodes[0].data)
        format = movie.getElementsByTagName('format')[0]
        print("Format: %s" % format.childNodes[0].data)
        rating = movie.getElementsByTagName('rating')[0]
        print("Rating: %s" % rating.childNodes[0].data)
        description = movie.getElementsByTagName('description')[0]
        print("Description: %s" % description.childNodes[0].data)

def test_10_json() :
    # Python 字典类型转换为 JSON 对象
    jsondata = {
        'no': 1,
        'name': 'Mythwind',
        'url': 'http://www.mythwind.com'
    }

    json_str = json.dumps(jsondata)
    print("Python 原始数据：", repr(jsondata))
    print("JSON 对象：", json_str)

    # 将 JSON 对象转换为 Python 字典
    data2 = json.loads(json_str)
    print("data2['name']: ", data2['name'])
    print("data2['url']: ", data2['url'])

    # 写入 JSON 数据
    with open(constants.FILE_JSON_DATA, 'w') as f:
        json.dump(jsondata, f)

    # 读取数据
    with open(constants.FILE_JSON_DATA, 'r') as f:
        data = json.load(f)
        print(data)

def test_matplot() :
    # fontproperties 设置中文显示，fontsize 设置字体大小
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # np.arange() 函数创建 x 轴上的值
    x = np.arange(-10, 10.1, 0.1, dtype=np.float)
    y = x * x

    plt.figure()
    plt.title("Matplotlib demo")
    plt.xlabel("x 轴")
    plt.ylabel("y 轴")
    # - 表示用画线来，如果是 ob =，则表示点
    plt.plot(x, y, '-')
    plt.show()

if __name__ == '__main__' :
    #test_01_regular()
    #test_02_cgi()
    #test_03_mysql()
    #test_04_pymysql()
    #test_05_network()
    #test_06_smtp()
    #test_07_multi_thread()
    #test_07_thread_queue()
    #test_08_xml_sax()
    #test_09_xml_dom()
    #test_10_json()
    test_matplot()
