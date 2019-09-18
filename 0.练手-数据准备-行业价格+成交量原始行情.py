from math import *
import numpy as np
import scipy.stats as stats
import pandas as pd
from pandas import Series, DataFrame
import datetime as dt
from sklearn import svm
from sklearn.linear_model.logistic import LogisticRegression 
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from lib.myFunction import *
 
pd.set_option('display.width', 200)

print 'Program started on: '+str(dt.datetime.now())

start = '2005-12-20'                       # 回测起始时间
end = '2017-12-31'                         # 回测结束时间

ASSET=['801010.ZICN','801020.ZICN','801030.ZICN','801040.ZICN','801050.ZICN','801060.ZICN','801070.ZICN','801080.ZICN','801090.ZICN','801100.ZICN','801110.ZICN','801120.ZICN','801130.ZICN','801140.ZICN','801150.ZICN','801160.ZICN','801170.ZICN','801180.ZICN','801190.ZICN','801200.ZICN','801210.ZICN','801220.ZICN','801230.ZICN','801710.ZICN','801720.ZICN','801730.ZICN','801740.ZICN','801750.ZICN','801760.ZICN','801770.ZICN','801780.ZICN','801790.ZICN','801880.ZICN','801890.ZICN']

#初始化时间节点
calList=getCalList('DAY',start,end,0,0)
print calList

#计算每个品种的累计日收益率序列
for facIte in ['closeIndex','turnoverVol']:
    histDaily=DataFrame(index=calList)
    histDailyDelta=DataFrame(index=calList)
    for objIte in ASSET:
        print '---- Fetch Industry Index history: ' + objIte        
        #获取历史序列
        histTmp=DataAPI.MktIdxdGet(indexID=objIte,beginDate=calList[0],endDate=calList[-1],field=u"tradeDate,"+facIte,pandas="1")
        histTmp.sort(columns='tradeDate',inplace=True)    
        histTmp.set_index('tradeDate',inplace=True)
        histTmp.columns=[objIte]
        histDaily=histDaily.merge(histTmp, how='left', left_index=True, right_index=True, copy=True) 
        #计算序列的日收益率
        histTmp[objIte]=(histTmp[objIte]/histTmp[objIte].shift(1)).apply(lambda x:log(x))
        histDailyDelta=histDailyDelta.merge(histTmp, how='left', left_index=True, right_index=True, copy=True) 

    #输出序列
    if facIte=='closeIndex':
        outputFile='Industry_Price.csv'   
        outputFile2='Industry_Price_Delta.csv'   
    if facIte=='turnoverVol':
        histDaily=histDaily.applymap(lambda x:1.0*x/100000000)
        outputFile='Industry_Turnover.csv'  
        outputFile2='Industry_Turnover_Delta.csv'   
    histDaily.to_csv(outputFile,index_label='tradeDate')        
    print 'Outpurt File: '+outputFile 
    histDailyDelta.to_csv(outputFile2,index_label='tradeDate')        
    print 'Outpurt File: '+outputFile2

print 'Program ended on: '+str(dt.datetime.now())