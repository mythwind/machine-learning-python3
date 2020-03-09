import numpy as np
import matplotlib.pyplot as plt
import tkinter


def plot_xycord(xcord, ycord) :
    fig = plt.figure()
    ax = fig.add_subplot(111)  # 添加subplot
    ax.scatter(xcord, ycord, s=20, c='blue', alpha=.5)  # 绘制样本点
    plt.title('dataset')  # 绘制title
    plt.xlabel('X')
    plt.show()


def plot_ex00_dataset(data_mat):
    n = len(data_mat)  # 数据个数
    # print(data_mat)
    xcord = []
    ycord = []  # 样本点
    for i in range(n):
        xcord.append(data_mat[i][0]);
        ycord.append(data_mat[i][1])  # 样本点
    plot_xycord(xcord, ycord)


def plot_ex0_dataset(data_mat):
    n = len(data_mat)  # 数据个数
    xcord = []  #样本点
    ycord = []  #样本点
    for i in range(n):
        xcord.append(data_mat[i][1])
        ycord.append(data_mat[i][2])        #样本点
    plot_xycord(xcord, ycord)



def plot_model_tree(data_mat,tree):
    n = len(data_mat)  # 数据个数
    # print(data_mat)
    xcord = []
    ycord = []  # 样本点
    xline1 = []; xline2 = []
    yline1 = []; yline2 = []
    for i in range(n):
        xcord.append(data_mat[i][0]);
        ycord.append(data_mat[i][1])  # 样本点
        if data_mat[i][0] <= tree['sp_val'] :
            xline1.append(data_mat[i][0])
            yline1.append(tree['right'].A[0][0] + tree['right'].A[1][0] * data_mat[i][0])
        else :
            xline2.append(data_mat[i][0])
            yline2.append(tree['left'].A[0][0] + tree['left'].A[1][0] * data_mat[i][0])
    fig = plt.figure()
    ax = fig.add_subplot(111)  # 添加subplot
    ax.plot(xline1, yline1, c='red')  # 绘制回归曲线
    ax.plot(xline2, yline2, c='red')  # 绘制回归曲线
    ax.scatter(xcord, ycord, s=20, c='blue', alpha=.5)  # 绘制样本点
    plt.title('dataset')  # 绘制title
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()


def bin_split_dataset(dataset, feature, value):
    """
    函数说明:根据特征切分数据集合
    Parameters:
        dataset - 数据集合
        feature - 带切分的特征
        value - 该特征的值
    Returns:
        mat0 - 切分的数据集合0
        mat1 - 切分的数据集合1
    """
    mat0 = dataset[np.nonzero(dataset[:, feature] > value)[0], :]
    mat1 = dataset[np.nonzero(dataset[:, feature] <= value)[0], :]
    return mat0, mat1


def reg_leaf(dataset):
    """
    生成叶结点
    :param dataset:
    :return:目标变量的均值
    """
    return np.mean(dataset[:, -1])


def reg_err(dataset):
    """
    误差估计函数
    :param dataset:
    :return: 目标变量的总方差
    """
    return np.var(dataset[:, -1]) * np.shape(dataset)[0]


def choose_best_split(dataset, leaf_type=reg_leaf, err_type=reg_err, ops=(1, 4)):
    # tolS允许的误差下降值,tolN切分的最少样本数
    tolS = ops[0];
    tolN = ops[1]
    # 如果当前所有值相等,则退出。(根据set的特性)
    if len(set(dataset[:, -1].T.tolist()[0])) == 1:
        return None, leaf_type(dataset)
    # 统计数据集合的行m和列n
    m, n = np.shape(dataset)
    # 默认最后一个特征为最佳切分特征,计算其误差估计
    S = err_type(dataset)
    # 分别为最佳误差,最佳特征切分的索引值,最佳特征值
    bestS = float('inf');
    bestIndex = 0;
    best_value = 0
    # 遍历所有特征列
    for featIndex in range(n - 1):
        # 遍历所有特征值
        for splitVal in set(dataset[:, featIndex].T.A.tolist()[0]):
            # 根据特征和特征值切分数据集
            mat0, mat1 = bin_split_dataset(dataset, featIndex, splitVal)
            # 如果数据少于tolN,则退出
            if (np.shape(mat0)[0] < tolN) or (np.shape(mat1)[0] < tolN): continue
            # 计算误差估计
            newS = err_type(mat0) + err_type(mat1)
            # 如果误差估计更小,则更新特征索引值和特征值
            if newS < bestS:
                best_index = featIndex
                best_value = splitVal
                bestS = newS
    # 如果误差减少不大则退出
    if (S - bestS) < tolS:
        return None, leaf_type(dataset)
    # 根据最佳的切分特征和特征值切分数据集合
    mat0, mat1 = bin_split_dataset(dataset, best_index, best_value)
    # 如果切分出的数据集很小则退出
    if (np.shape(mat0)[0] < tolN) or (np.shape(mat1)[0] < tolN):
        return None, leaf_type(dataset)
    # 返回最佳切分特征和特征值
    return best_index, best_value


def create_tree(dataset, leaf_type=reg_leaf, err_type=reg_err, ops=(1, 4)):
    """
    树构建函数
    :param dataset:
    :param leaf_type:
    :param err_type:
    :param ops:
    :return:
    """
    # 选择最佳切分特征和特征值
    feat, val = choose_best_split(dataset, leaf_type, err_type, ops)
    # print("tree_regres:\n", feat, val)
    # 如果没有特征,则返回特征值
    if feat == None:
        return val
    ret_tree = {}
    ret_tree['sp_ind'] = feat
    ret_tree['sp_val'] = val
    # 分成左数据集和右数据集
    lset, rset = bin_split_dataset(dataset, feat, val)
    # 创建左子树和右子树
    ret_tree['left'] = create_tree(lset, leaf_type, err_type, ops)
    ret_tree['right'] = create_tree(rset, leaf_type, err_type, ops)
    return ret_tree


def is_tree(obj) :
    """
    判断测试输入变量是否是一棵树
    :param obj:
    :return:
    """
    return (type(obj).__name__ == 'dict')

def get_tree_mean(tree) :
    """
    对树进行塌陷处理(即返回树平均值)
    :param tree:
    :return:
    """
    if is_tree(tree['right']) :
        tree['right'] = get_tree_mean(tree['right'])
    if is_tree(tree['left']):
        tree['left'] = get_tree_mean(tree['left'])
    return (tree['left'] + tree['right']) / 2.0

def prune(tree, test_data) :
    """
    后剪枝
    :param tree:
    :param test_data:
    :return:
    """
    # 如果测试集为空,则对树进行塌陷处理
    if np.shape(test_data)[0] == 0:
        return get_tree_mean(tree)
    # 如果有左子树或者右子树,则切分数据集
    if is_tree(tree['left']) or is_tree(tree['right']) :
        lset, rset = bin_split_dataset(test_data, tree['sp_ind'], tree['sp_val'])
    # 处理左子树(剪枝)
    if is_tree(tree['left']):
        tree['left'] = prune(tree['left'], lset)
    # 处理右子树(剪枝)
    if is_tree(tree['right']):
        tree['right'] = prune(tree['right'], rset)
    # 如果当前结点的左右结点为叶结点
    if not is_tree(tree['left']) and not is_tree(tree['right']):
        lset, rset = bin_split_dataset(test_data, tree['sp_ind'], tree['sp_val'])
        # 计算没有合并的误差
        error_no_merge = np.sum(np.power(lset[:, -1] - tree['left'], 2)) + np.sum(np.power(rset[:, -1] - tree['right'], 2))
        # 计算合并的均值
        tree_mean = (tree['left'] + tree['right']) / 2.0
        # 计算合并的误差
        error_merge = np.sum(np.power(test_data[:, -1] - tree_mean, 2))
        # 如果合并的误差小于没有合并的误差,则合并
        if error_merge < error_no_merge:
            return tree_mean
        else:
            return tree
    else:
        return tree


def linear_solve(dataset) :
    """
    数据集格式化为目标变量Y和自变量X
    :param dataset:
    :return:
    """
    m,n = np.shape(dataset)
    X = np.mat(np.ones((m, n)))
    Y = np.mat(np.ones((m, 1)))
    X[:,1:n] = dataset[:,0:n - 1]
    Y = dataset[:,-1]
    xtx = X.T * X
    if np.linalg.det(xtx) == 0.0 :
        raise NameError("矩阵为奇异矩阵,不能求逆,请尝试增加ops的值")
    ws = xtx.I * (X.T * Y)
    return ws, X, Y

def  model_leaf(dataset) :
    ws, X, Y = linear_solve(dataset)
    return ws

def model_error(dataset) :
    ws, X, Y = linear_solve(dataset)
    yhat = X * ws
    return sum(np.power(Y - yhat, 2))


def reg_tree_eval(model, indat) :
    return float(model)

def model_tree_eval(model, indat) :
    n = np.shape(indat)[1]
    X = np.mat(np.ones(1, n + 1))
    X[: , 1 : n + 1] = indat
    return float(X * model)


def tree_forecast(tree, indata, model_eval = reg_tree_eval) :
    if not is_tree(tree) :
        return model_eval(tree, indata)
    if indata[tree['sp_ind']] > tree['sp_val'] :
        if is_tree(tree['left']) :
            return tree_forecast(tree['left'], indata, model_eval)
        else :
            return model_eval(tree['left'], indata)
    else :
        if is_tree(tree['right']) :
            return tree_forecast(tree['right'], indata, model_eval)
        else :
            return model_eval(tree['right'], indata)

def create_forecast(tree, test_data, model_eval = reg_tree_eval) :
    m = len(test_data)
    yhat = np.mat(np.zeros((m, 1)))
    for i in range(m) :
        yhat[i,0] = tree_forecast(tree, np.mat(test_data[i]), model_eval)
    return yhat


def draw_new_tree() :
    pass

def redraw(tols,toln) :
    #redraw.f.clf()
    #redraw.a = redraw.f.add_subplot(111)
    pass


def test_tkinter() :
    root = tkinter.Tk()
    tkinter.Label(root, text="Plot Place Holder").grid(row=0, columnspan=3)
    tkinter.Label(root, text="tolN").grid(row=1, column=0)
    toln_entry = tkinter.Entry(root)
    toln_entry.grid(row=1, column=1)
    toln_entry.insert(0, '10')
    tkinter.Label(root, text="tolS").grid(row=2, column=0)
    tols_entry = tkinter.Entry(root)
    tols_entry.grid(row=2, column=1)
    tols_entry.insert(0, '1.0')
    tkinter.Button(root, text="ReDraw", command=draw_new_tree).grid(row=1, column=2, columnspan=3)

    chk_btn_var = tkinter.IntVar()
    chk_btn = tkinter.Checkbutton(root, text="Model Tree", variable=chk_btn_var)
    chk_btn.grid(row=3, column=0, columnspan=2)

    redraw(1.0, 10)
    root.mainloop()

