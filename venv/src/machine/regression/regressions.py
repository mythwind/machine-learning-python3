import matplotlib.pyplot as plt
import numpy as np
import random
from bs4 import BeautifulSoup

def plot_data(xarr, yarr) :
    n = len(xarr)  # 数据个数
    xcord = []
    ycord = []  # 样本点
    for i in range(n):
        xcord.append(xarr[i][1])
        ycord.append(yarr[i])  # 样本点
    fig = plt.figure()
    ax = fig.add_subplot(111)  # 添加subplot
    ax.scatter(xcord, ycord, s=20, c='blue', alpha=.5)  # 绘制样本点
    plt.title('DataSet')
    plt.show()

def plot_data_ws(xmat, ymat, ws) :
    fig = plt.figure()
    ax = fig.add_subplot(111)  # 添加subplot
    # 绘制原始数据？
    # a=mat([[1,2,3],[4,5,6]])
    # a.flatten().A[0]  array([1, 2, 3, 4, 5, 6])
    ax.scatter(xmat[:,1].flatten().A[0], ymat.T[:,0].flatten().A[0])
    xcopy = xmat.copy()
    xcopy.sort(0)
    ax.plot(xcopy[:,1], xcopy * ws)
    plt.title('DataSet')
    plt.show()

def plot_lwlr_regression(xarr,yarr):
    """
    函数说明:绘制多条局部加权回归曲线
    """
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签 
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    yhat_1 = lwlr_forecast_yhat(xarr, xarr, yarr, 1.0)         #根据局部加权线性回归计算yHat
    yhat_2 = lwlr_forecast_yhat(xarr, xarr, yarr, 0.01)        #根据局部加权线性回归计算yHat
    yhat_3 = lwlr_forecast_yhat(xarr, xarr, yarr, 0.003)       #根据局部加权线性回归计算yHat
    xmat = np.mat(xarr)                                                    #创建xMat矩阵
    ymat = np.mat(yarr)                                                    #创建yMat矩阵
    srtInd = xmat[:, 1].argsort(0)                                        #排序，返回索引值
    xSort = xmat[srtInd][:,0,:]
    fig, axs = plt.subplots(nrows=3, ncols=1,sharex=False, sharey=False, figsize=(10,8))
    axs[0].plot(xSort[:, 1], yhat_1[srtInd], c = 'red')                        #绘制回归曲线
    axs[1].plot(xSort[:, 1], yhat_2[srtInd], c = 'red')                        #绘制回归曲线
    axs[2].plot(xSort[:, 1], yhat_3[srtInd], c = 'red')                        #绘制回归曲线
    axs[0].scatter(xmat[:,1].flatten().A[0], ymat.flatten().A[0], s = 20, c = 'blue', alpha = .5)                #绘制样本点
    axs[1].scatter(xmat[:,1].flatten().A[0], ymat.flatten().A[0], s = 20, c = 'blue', alpha = .5)                #绘制样本点
    axs[2].scatter(xmat[:,1].flatten().A[0], ymat.flatten().A[0], s = 20, c = 'blue', alpha = .5)                #绘制样本点
    #设置标题,x轴label,y轴label
    axs0_title_text = axs[0].set_title(u'局部加权回归曲线,k=1.0')
    axs1_title_text = axs[1].set_title(u'局部加权回归曲线,k=0.01')
    axs2_title_text = axs[2].set_title(u'局部加权回归曲线,k=0.003')
    plt.setp(axs0_title_text, size=8, weight='bold', color='red')
    plt.setp(axs1_title_text, size=8, weight='bold', color='red')
    plt.setp(axs2_title_text, size=8, weight='bold', color='red')
    plt.xlabel('X')
    plt.show()


def plot_ridge_regression(ridge_weight):
    """
    函数说明:绘制岭回归曲线
    """
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签 
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(ridge_weight)
    ax_title_text = ax.set_title(u'log(lambada)与回归系数的关系')
    ax_xlabel_text = ax.set_xlabel(u'log(lambada)')
    ax_ylabel_text = ax.set_ylabel(u'回归系数')
    plt.setp(ax_title_text, size=20, weight='bold', color='red')
    plt.setp(ax_xlabel_text, size=10, weight='bold', color='black')
    plt.setp(ax_ylabel_text, size=10, weight='bold', color='black')
    plt.show()



def plot_stage_wise(return_mat):
    """
    函数说明:绘制岭回归曲线
    """
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签 
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(return_mat)
    ax_title_text = ax.set_title(u'前向逐步回归:迭代次数与回归系数的关系')
    ax_xlabel_text = ax.set_xlabel(u'迭代次数')
    ax_ylabel_text = ax.set_ylabel(u'回归系数')
    plt.setp(ax_title_text, size=15, weight='bold', color='red')
    plt.setp(ax_xlabel_text, size=10, weight='bold', color='black')
    plt.setp(ax_ylabel_text, size=10, weight='bold', color='black')
    plt.show()


"""
计算回归系数ws
平方误差公式：w=(XᵀX)⁻¹Xᵀy 其中X必须为方阵，求逆
"""
def stand_regres(xarr, yarr) :
    xmatrix = np.mat(xarr)
    ymatrix = np.mat(yarr).T
    # 根据文中推导的公示计算回归系数， 矩阵转置*矩阵=对称阵
    # 若x为向量，则默认x为列向量，x^T为行向量
    xtx = xmatrix.T * xmatrix
    if np.linalg.det(xtx) == 0.0 :
        print("矩阵为奇异矩阵,不能求逆")
        return
    ws = xtx.I * (xmatrix.T * ymatrix)
    return ws

"""
局部加权线性回归计算回归系数w
w=(XᵀWX)⁻¹XᵀWy 
"""
def lwlr_regres(test_point,xarr, yarr,k=1.0) :
    xmatrix = np.mat(xarr)
    ymatrix = np.mat(yarr).T
    m = np.shape(xmatrix)[0]
    # np.eye 表示单位对角矩阵
    weights = np.mat(np.eye((m)))
    for j in range(m) :
        diff_mat = test_point - xmatrix[j,:]
        weights[j,j] = np.exp(diff_mat * diff_mat.T / (-2.0 * k ** 2))
    xtx = xmatrix.T * (weights * xmatrix)
    if np.linalg.det(xtx) == 0.0 :
        print("矩阵为奇异矩阵,不能求逆")
        return
    ws = xtx.I * (xmatrix.T * (weights * ymatrix))
    return test_point * ws

def lwlr_forecast_yhat(test_arr,xarr, yarr,k=1.0) :
    m = np.shape(test_arr)[0]
    yhat = np.zeros(m)
    for i in range(m) :
        yhat[i] = lwlr_regres(test_arr[i],xarr,yarr,k)
    return yhat

"""
岭回归：w=(XᵀX + αI)⁻¹Xᵀy
"""
def ridge_regres(xmat,ymat,lam=0.2) :
    xtx = xmat.T * xmat
    denom = xtx + np.eye(np.shape(xmat)[1]) * lam
    if np.linalg.det(denom) == 0.0 :
        print("矩阵为奇异矩阵,不能求逆")
        return
    ws = denom.I * (xmat.T * ymat)
    return ws


def ridge_test(xarr,yarr) :
    xmat = np.mat(xarr)
    ymat = np.mat(yarr).T
    ymean = np.mean(ymat,0)
    ymat = ymat - ymean
    xmean = np.mean(xmat,0)
    xvar = np.var(xmat,0)
    xmat = (xmat - xmean) / xvar
    num_pts = 30
    wmat = np.zeros((num_pts, np.shape(xmat)[1]))
    for i in range(num_pts) :
        ws = ridge_regres(xmat,ymat,np.exp(i-10))
        wmat[i,:] = ws.T
    return wmat


def regularize(xmat):#regularize by columns
    inmat = xmat.copy()
    inmeans = np.mean(inmat,0)   #calc mean then subtract it off
    invar = np.var(inmat,0)      #calc variance of Xi then divide by it
    inmat = (inmat - inmeans) / invar
    return inmat

"""
前向逐步回归
"""
def stage_wise(xarr,yarr,eps=0.01,num_iter=100) :
    xmat = np.mat(xarr)
    ymat = np.mat(yarr).T
    ymean = np.mean(ymat, 0)
    ymat = ymat - ymean
    xmat = regularize(xmat)
    m,n = np.shape(xmat)
    return_mat = np.zeros((num_iter,n))
    ws = np.zeros((n, 1))
    ws_test = ws.copy()
    ws_max = ws.copy()
    for i in range(num_iter) :
        # print(ws.T)
        lowest_error = np.inf;
        for j in range(n):
            for sign in [-1, 1]:
                ws_test = ws.copy()
                ws_test[j] += eps * sign
                ytest = xmat * ws_test
                rss_err = rss_error(ymat.A, ytest.A)
                if rss_err < lowest_error:
                    lowest_error = rss_err
                    ws_max = ws_test
        ws = ws_max.copy()
        return_mat[i,:] = ws.T
    return return_mat

"""
误差大小评价函数
Parameters:
    yArr - 真实数据
    yHatArr - 预测数据
Returns:
    误差大小
"""
def rss_error(yarr, yhat_arr):
    return ((yarr - yhat_arr) ** 2).sum()

"""
函数说明:从页面读取数据，生成retX和retY列表
"""
def scrapy_page(retX, retY, infile, yr, num_pce, orig_pric) :
    with open(infile,encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html)
    i = 1
    # 根据HTML页面结构进行解析
    current_row = soup.find_all('table', r="%d" % i)
    while (len(current_row) != 0) :
        current_row = soup.find_all('table', r="%d" % i)
        title = current_row[0].find_all('a')[1].text
        lwr_title = title.lower()
        # 查找是否有全新标签
        if (lwr_title.find('new') > -1) or (lwr_title.find('nisb') > -1):
            new_flag = 1.0
        else:
            new_flag = 0.0
        # 查找是否已经标志出售，我们只收集已出售的数据
        sold_unicde = current_row[0].find_all('td')[3].find_all('span')
        if len(sold_unicde) == 0:
            print("商品 #%d 没有出售" % i)
        else:
            # 解析页面获取当前价格
            sold_price = current_row[0].find_all('td')[4]
            price_str = sold_price.text
            price_str = price_str.replace('$', '').replace(',', '')
            if len(sold_price) > 1:
                price_str = price_str.replace('Free shipping', '')
            selling_price = float(price_str)
            # 去掉不完整的套装价格
            if selling_price > orig_pric * 0.5:
                print("%d\t%d\t%d\t%f\t%f" % (yr, num_pce, new_flag, orig_pric, selling_price))
                retX.append([yr, num_pce, new_flag, orig_pric])
                retY.append(selling_price)
        i += 1
        current_row = soup.find_all('table', r="%d" % i)

"""
依次读取六种乐高套装的数据，并生成数据矩阵
"""
def set_data_collect(retX,retY) :
    scrapy_page(retX, retY, 'assets/lego/lego8288.html', 2006, 800, 49.99)  # 2006年的乐高8288,部件数目800,原价49.99
    scrapy_page(retX, retY, 'assets/lego/lego10030.html', 2002, 3096, 269.99)  # 2002年的乐高10030,部件数目3096,原价269.99
    scrapy_page(retX, retY, 'assets/lego/lego10179.html', 2007, 5195, 499.99)  # 2007年的乐高10179,部件数目5195,原价499.99
    scrapy_page(retX, retY, 'assets/lego/lego10181.html', 2007, 3428, 199.99)  # 2007年的乐高10181,部件数目3428,原价199.99
    scrapy_page(retX, retY, 'assets/lego/lego10189.html', 2008, 5922, 299.99)  # 2008年的乐高10189,部件数目5922,原价299.99
    scrapy_page(retX, retY, 'assets/lego/lego10196.html', 2009, 3263, 249.99)  # 2009年的乐高10196,部件数目3263,原价249.99

def cross_validation(xarr,yarr,num_val = 10) :
    """
    交叉验证岭回归
    :param xarr:
    :param yarr:
    :param num_val:
    :return:
    """
    m = len(yarr)
    index_list = list(range(m))
    error_matrix = np.zeros((num_val,30))
    for i in range(num_val) :
        trainX = [];
        trainY = []  # 训练集
        testX = [];
        testY = []  # 测试集
        random.shuffle(index_list)
        for j in range(m):  # 划分数据集:90%训练集，10%测试集
            if j < m * 0.9:
                trainX.append(xarr[index_list[j]])
                trainY.append(yarr[index_list[j]])
            else:
                testX.append(xarr[index_list[j]])
                testY.append(yarr[index_list[j]])
        wMat = ridge_test(trainX, trainY)  # 获得30个不同lambda下的岭回归系数
        for k in range(30):  # 遍历所有的岭回归系数
            mat_testX = np.mat(testX);
            mat_trainX = np.mat(trainX)  # 测试集
            mean_train = np.mean(mat_trainX, 0)  # 测试集均值
            var_train = np.var(mat_trainX, 0)  # 测试集方差
            mat_testX = (mat_testX - mean_train) / var_train  # 测试集标准化
            yEst = mat_testX * np.mat(wMat[k, :]).T + np.mean(trainY)  # 根据ws预测y值
            error_matrix[i, k] = rss_error(yEst.T.A, np.array(testY))
    meanErrors = np.mean(error_matrix,0)                                                    #计算每次交叉验证的平均误差
    minMean = float(min(meanErrors))                                                    #找到最小误差
    bestWeights = wMat[np.nonzero(meanErrors == minMean)]                                #找到最佳回归系数
    xMat = np.mat(xarr);
    yMat = np.mat(yarr).T
    meanX = np.mean(xMat,0);
    varX = np.var(xMat,0)
    unReg = bestWeights / varX                                                            #数据经过标准化，因此需要还原
    print('%f%+f*年份%+f*部件数量%+f*是否为全新%+f*原价' % ((-1 * np.sum(np.multiply(meanX,unReg)) + np.mean(yMat)), unReg[0,0], unReg[0,1], unReg[0,2], unReg[0,3]))
