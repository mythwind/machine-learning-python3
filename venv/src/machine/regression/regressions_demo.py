import machine.constants as consts
import utils.file_utils as file_utils
import regression.regressions as regressions
import numpy as np

def test_data() :
    xarr, yarr = file_utils.load_dataset_from_file(consts.FILE_REGRESSION_0_PATH)
    # regressions.plot_data(xarr, yarr)
    ws = regressions.stand_regres(xarr,yarr)
    # print(ws)
    xmat = np.mat(xarr)
    ymat = np.mat(yarr)
    yhat = xmat * ws
    # print(np.corrcoef(yhat.T, ymat))
    regressions.plot_data_ws(xmat,ymat,ws)

def test_lwlr() :
    xarr, yarr = file_utils.load_dataset_from_file(consts.FILE_REGRESSION_0_PATH)
    ws = regressions.lwlr_regres(xarr[0],xarr,yarr,1.0)
    print("ws 1.0:\n",ws)

    regressions.plot_lwlr_regression(xarr,yarr)

def test_abalone() :
    abX, abY = file_utils.load_dataset_from_file(consts.FILE_REGRESSION_ABALONE_PATH)
    print('训练集与测试集相同:局部加权线性回归,核k的大小对预测的影响:')
    yHat01 = regressions.lwlr_forecast_yhat(abX[0:99], abX[0:99], abY[0:99], 0.1)
    yHat1 = regressions.lwlr_forecast_yhat(abX[0:99], abX[0:99], abY[0:99], 1)
    yHat10 = regressions.lwlr_forecast_yhat(abX[0:99], abX[0:99], abY[0:99], 10)
    print('k=0.1时,误差大小为:', regressions.rss_error(abY[0:99], yHat01.T))
    print('k=1  时,误差大小为:', regressions.rss_error(abY[0:99], yHat1.T))
    print('k=10 时,误差大小为:', regressions.rss_error(abY[0:99], yHat10.T))
    print('')
    print('训练集与测试集不同:局部加权线性回归,核k的大小是越小越好吗？更换数据集,测试结果如下:')
    yHat01 = regressions.lwlr_forecast_yhat(abX[100:199], abX[0:99], abY[0:99], 0.1)
    yHat1 = regressions.lwlr_forecast_yhat(abX[100:199], abX[0:99], abY[0:99], 1)
    yHat10 = regressions.lwlr_forecast_yhat(abX[100:199], abX[0:99], abY[0:99], 10)
    print('k=0.1时,误差大小为:', regressions.rss_error(abY[100:199], yHat01.T))
    print('k=1  时,误差大小为:', regressions.rss_error(abY[100:199], yHat1.T))
    print('k=10 时,误差大小为:', regressions.rss_error(abY[100:199], yHat10.T))
    print('')

    ridge_weight = regressions.ridge_test(abX,abY)
    print("ridge_weight : \n", ridge_weight)
    regressions.plot_ridge_regression(ridge_weight)

def test_stage_wise() :
    abX, abY = file_utils.load_dataset_from_file(consts.FILE_REGRESSION_ABALONE_PATH)
    return_mat = regressions.stage_wise(abX,abY,0.01,200)
    #print(return_mat)
    regressions.plot_stage_wise(return_mat)

    return_mat = regressions.stage_wise(abX, abY, 0.001, 5000)
    #print(return_mat)
    regressions.plot_stage_wise(return_mat)

def test_lego() :
    lgX = []
    lgY = []
    regressions.set_data_collect(lgX, lgY)
    data_num, features_num = np.shape(lgX)
    lgX1 = np.mat(np.ones((data_num, features_num + 1)))
    lgX1[:, 1:5] = np.mat(lgX)
    ws = regressions.stand_regres(lgX1, lgY)
    print('%f%+f*年份%+f*部件数量%+f*是否为全新%+f*原价' % (ws[0], ws[1], ws[2], ws[3], ws[4]))
    print("===============")
    print(regressions.ridge_test(lgX,lgY))

if __name__ == '__main__' :
    # test_data()
    # test_lwlr()
    # test_abalone()
    # test_stage_wise()
    test_lego()
