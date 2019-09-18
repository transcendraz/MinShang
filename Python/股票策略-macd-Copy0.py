
# coding: utf-8

# In[ ]:

import pandas as pd
import talib as ta
import numpy as np
import time
from datetime import date,timedelta
import lib.stock_strategy as strategy
#指数行业 分析
#index0=pd.read_csv('do/gz_indexID.csv',encoding='gbk')
index0=pd.read_csv('do/gz_indexID.csv',encoding='gbk')
print index0.columns
t=index0.columns[2]
index0=index0[index0[t]==1]
index=index0.secID.tolist()
#index=["000016.ZICN","399005.ZICN","399006.ZICN","000905.ZICN","000906.ZICN","000300.ZICN"] #宽基指数
#index=["399372.ZICN","399373.ZICN", "399374.ZICN", "399375.ZICN", "399376.ZICN", "399377.ZICN"] #风格指数
#index=["000801.ZICN","000806.ZICN","000807.ZICN","000808.ZICN","000809.ZICN","000810.ZICN","000811.ZICN","000812.ZICN","000813.ZICN","000814.ZICN","000815.ZICN","000816.ZICN","000819.ZICN","000820.ZICN"] #行业指数
#index=["000928.ZICN","000929.ZICN","000930.ZICN","000931.ZICN","000932.ZICN","000933.ZICN","000934.ZICN","000935.ZICN","000936.ZICN","000937.ZICN","000942.ZICN","000943.ZICN","000944.ZICN","000945.ZICN","000946.ZICN","000947.ZICN","000948.ZICN","000949.ZICN"] #行业指数

#index=["000300.ZICN"]
allindex=pd.DataFrame()
for i in range(len(index)):
    df_index=DataAPI.MktIdxdGet(tradeDate=u"",indexID=index[i],ticker=u"",beginDate=u"20160101",endDate=u"",exchangeCD=u"XSHE,XSHG",field=u"",pandas="1")
    df_index["openPrice"]=df_index["openIndex"]
    df_index["lowestPrice"]=df_index["lowestIndex"]
    df_index["highestPrice"]=df_index["highestIndex"]
    df_index["closePrice"]=df_index["closeIndex"]
    df_index.rename(columns={'indexID':'secID'},inplace=True)
    df_index_curve=strategy.mslope(df_index)
    #z=strategy.day2week(df_index)
    #df_index_curve=strategy.mslope(z)
    #df_index_curve=strategy.Macd_strategy(df_index)
    #df_index_curve=strategy.Macd_strategy(z)
    allindex=allindex.append(df_index_curve)
#allindex.rename(columns={'indexID': 'secID'}, inplace=True) 
    
allindex.sort_values(by=['tradeDate'], inplace=True)
d=allindex[["secID","tradeDate","signal",'equity_curve']]
d.sort_values(by=["tradeDate",'secID'], inplace=True)

#a.to_csv('do/indexindstry1w_macd.csv',encoding='gbk')
all_IndexID=DataAPI.MktIdxdGet(tradeDate=u"20171229",indexID=u"",ticker=u"",beginDate=u"",endDate=u"",exchangeCD=u"XSHE,XSHG",field=u"indexID,secShortName",pandas="1")
all_IndexID.rename(columns={'indexID':'secID'},inplace=True)
d=pd.merge(d,all_IndexID, how='inner', on=['secID'])
pivot_d=pd.pivot_table(d, values='signal', index=['tradeDate'], columns=['secShortName'], aggfunc=np.sum)
name="do/gz_" + t +".csv"
pivot_d.to_csv(name,encoding='gbk')
pivot_d.tail()


# In[ ]:

Y_in=pivot_d
X_in=Y_in.loc['2018-01-23']
X1_in=X_in.reset_index()
X1_in.columns=["secShortName","signal"]
X1_in[X1_in['signal']==1]


# In[ ]:

#d.groupby(['tradeDate'])['equity_curve'].mean()
#all_IndexID.to_csv('do/gz.csv',encoding='gbk')


# In[ ]:

index=["000016.ZICN","399005.ZICN","399006.ZICN","000905.ZICN","000906.ZICN","000300.ZICN"]
xstock_ID=DataAPI.IdxConsGet(secID=index[2],ticker=u"",intoDate=u"20161231",isNew=u"",field=u"",pandas="1")
#xstock_ID=DataAPI.IdxConsGet(secID=u"399401",ticker=u"",intoDate=u"",isNew=u"",field=u"",pandas="1")
xstock_ID=xstock_ID[['consID','consShortName']]
xstock_ID.rename(columns={'consID':'secID'},inplace=True)
Cons_ID=DataAPI.EquGet(equTypeCD=u"A",secID=u"",ticker=u"",listStatusCD=u"",field=u"secID,listDate",pandas="1")
xstock_ID=xstock_ID.merge(Cons_ID,how='inner',on='secID')
xstock_ID=xstock_ID[xstock_ID['listDate']<='2016-01-01']
stock_stop=DataAPI.MktEqudGet(tradeDate=u"20171229",secID=xstock_ID.secID.tolist(),ticker=u"",beginDate=u"",endDate=u"",isOpen="1",field=u"secID,isOpen",pandas="1")
xstock_ID=xstock_ID.merge(stock_stop,how='inner',on='secID')

#xstock_ID=xstock_ID.drop(42) #上市时间
ID=xstock_ID.secID.tolist()

#由于数据量有限制，一次调用50个基金数据
#for i in range(len(ID)):
num_up=20
num=len(ID)/num_up+1
xstock=pd.DataFrame()        #df_stock=DataAPI.MktEqudGet(tradeDate=u"",secID=ID[i],ticker=u"",beginDate=u"20160101",endDate=u"",isOpen="",field=u"",pandas="1")
if num > 1:
    for i in range(num):
        
        for j in range(len(ID[i*num_up:(i+1)*num_up])):
            
            df_stock=DataAPI.MktEqudGet(tradeDate=u"",secID=ID[i*num_up:(i+1)*num_up][j],ticker=u"",beginDate=u"20170101",endDate=u"",isOpen="",field=u"",pandas="1")
            a1=strategy.fuquan(df_stock)
            a=strategy.day2week(a1)
            #print a
            df_stock_curve=strategy.mslope(df_stock)
            xstock=pd.concat([xstock,df_stock_curve])
else:
    for k in range(len(ID)):
        df_stock=DataAPI.MktEqudGet(tradeDate=u"",secID=ID[k],ticker=u"",beginDate=u"20170101",endDate=u"",isOpen="",field=u"",pandas="1")
        a1=strategy.fuquan(df_stock)
        a=strategy.day2week(a1)
        df_stock_curve=strategy.mslope(a)
        xstock=pd.concat([xstock,df_stock_curve])
xstock        


#xstock_curve["tradeDate"]=pd.to_datetime(xstock_curve["tradeDate"])
xstock=xstock.sort_values(by=['tradeDate'], inplace=True)
ds=xstock[["secID","tradeDate","secShortName","signal",'equity_curve']]
ds.sort_values(by=['secID',"tradeDate"], inplace=True)
#print len(ds[ds['tradeDate']=='2018-01-04'])
#print ds[ds['tradeDate']=='2018-01-04']
#xstock.groupby(['tradeDate'])['equity_curve'].mean()


# In[ ]:

xstock


# In[ ]:

Y=pd.pivot_table(ds, values='signal', index=['tradeDate'], columns=['secShortName'], aggfunc=np.sum)
X=Y.loc['2018-01-22']
X1=X.reset_index()
X1.columns=["secShortName","signal"]
X1[X1['signal']==1]


#ds.groupby(['tradeDate'])['equity_curve'].mean()


# In[ ]:

ds.groupby(['tradeDate'])['equity_curve'].mean()


# In[ ]:

a=DataAPI.MktEqudGet(tradeDate=u"",secID=u"",ticker=u"601229",beginDate=u"20060101",endDate=u"",isOpen="",field=u"",pandas="1")
a1=strategy.fuquan(a)
b=strategy.day2week(a1)
strategy.mslope(b)


# In[ ]:

import pandas as pd
a=DataAPI.MktIdxdGet(tradeDate=u"20171229",indexID=u"",ticker=u"",beginDate=u"",endDate=u"",exchangeCD=u"XSHE,XSHG",field=u"",pandas="1")

a.to_csv("index001.csv",encoding="gbk")


# In[ ]:

xstock.groupby(['tradeDate'])['equity_curve'].mean()


# In[ ]:

a=DataAPI.MktIdxdGet(tradeDate=u"20171208",indexID=u"",ticker=u"",beginDate=u"",endDate=u"",exchangeCD=u"XSHE,XSHG",field=u"",pandas="1")
a.columns
a["openPrice"]=a["openIndex"]
a["lowestPrice"]=a["lowestIndex"]
a["highestPrice"]=a["highestIndex"]
a["closePrice"]=a["closeIndex"]


# In[ ]:

a=DataAPI.MktIdxdGet(tradeDate=u"20171208",indexID=u"",ticker=u"",beginDate=u"",endDate=u"",exchangeCD=u"XSHE,XSHG",field=u"",pandas="1")
a.to_csv("do/indexID.csv",encoding="gbk")


# In[ ]:

#df_future=DataAPI.MktMFutdGet(tradeDate=u"",mainCon=u"",contractMark=u"",contractObject=u"JM",startDate=u"",endDate=u"",field=u"",pandas="1")
df_future=DataAPI.MktEqudGet(tradeDate=u"",secID=u"",ticker=u"600570",beginDate=u"",endDate=u"",isOpen="",field=u"secID,tradeDate,openPrice,highestPrice,lowestPrice,closePrice,turnoverVol,chgPct,isOpen",pandas="1")
df_future["tradeDate"]=pd.to_datetime(df_future["tradeDate"])
df_future.sort_values(by=['tradeDate'], inplace=True)
#df_future=df_future[(df_future["mainCon"]==1)]
df_future["closePrice"]=pd.DataFrame(df_future["closePrice"],dtype="float")
df_future
a=strategy.mslope(strategy.day2week(df_future))
#a1=strategy.mslope(df_future)
#a=Macd_strategy(strategy.day2week(df_future))
#a1=DMacd_strategy(strategy.day2week(df_future))
#a1=DMacd_strategy(df_future)
#a.to_csv("do/future.csv")
#a
t=a1.tradeDate.tolist()
y=a1.equity_curve.values
y=a1.equity_curve.values
strategy.sinplot("a","b","c","d",t,y,y)
a1


# In[ ]:




# In[ ]:

t


# In[ ]:





# In[ ]:

Close_table=pd.pivot_table(Socre, values='turnoOverValue', index=['tradeDate'], columns=['secID'], aggfunc=np.sum)
Close_table


# In[ ]:




# In[ ]:

DataAPI.MktIdxdGet(tradeDate=u"",indexID=u"",ticker=u"000300",beginDate=u"20171208",endDate=u"",exchangeCD=u"XSHE,XSHG",field=u"",pandas="1")


# In[ ]:

#HS300指数成分股
df_stock=DataAPI.MktEqudGet(tradeDate=u"",secID=u"",ticker=u"600570",beginDate=u"",endDate=u"",isOpen="",field=u"secID,tradeDate,openPrice,highestPrice,lowestPrice,closePrice,turnoverVol,chgPct",pandas="1")
#基金
df_etffund=DataAPI.MktFunddAdjGet(secID=u"",ticker=u"510050",beginDate=u"20150901",endDate=u"20150901",field=u"",pandas="1")
#指数
df_index=DataAPI.MktIdxdGet(tradeDate=u"20161219",indexID=u"",ticker=u"",beginDate=u"",endDate=u"",exchangeCD=u"XSHE,XSHG",field=u"",pandas="1")

df_future=DataAPI.MktFutdVolGet(secID=u"",ticker=u"fu1512",beginDate=u"20150310",endDate=u"",field=u"",pandas="1")


# In[ ]:

df_index=DataAPI.MktIdxdGet(tradeDate=u"",indexID=u"",ticker=u"000300",beginDate=u"",endDate=u"",exchangeCD=u"XSHE,XSHG",field=u"",pandas="1")
df_index.head()
df_index=df_index[["indexID","secShortName","tradeDate","openIndex","lowestIndex","highestIndex","closeIndex","turnoverVol","CHGPct"]]
df_index.columns=["indexID","secShortName","tradeDate","openPrice","lowestPrice","highestPrice","closePrice","turnoverVol","CHGPct"]
a=mslope(day2week(df_index))
t=a.tradeDate.tolist()
y=a.equity_curve.values
sinplot("retrun","time","hs300","time",t,y)
a


# In[ ]:

b=DataAPI.MktIdxdGet(tradeDate=u"20171215",indexID=u"",ticker=u"",beginDate=u"",endDate=u"",exchangeCD=u"XSHE,XSHG",field=u"",pandas="1")
b.to_csv("do/index.csv",encoding="gbk")


# In[ ]:

df_etffund=DataAPI.MktFunddAdjGet(secID=u"",ticker=u"513500",beginDate=u"",endDate=u"",field=u"",pandas="1")
a=mslope(day2week(df_etffund))
t=a.tradeDate.tolist()
y=a.equity_curve.values
sinplot("a","b","c","d",t,y)


# In[ ]:

df_future=DataAPI.MktFutdVolGet(secID=u"",ticker=u"fu1512",beginDate=u"",endDate=u"",field=u"",pandas="1")

#a=mslope(df_future)
df_future

#t=a.tradeDate.tolist()
#y=a.equity_curve.values
#sinplot("a","b","c","d",t,y)


# In[ ]:

df_etffund=DataAPI.MktFunddAdjGet(secID=u"",ticker=u"",beginDate=u"20171215",endDate=u"20171215",field=u"",pandas="1")
df_etffund=df_etffund[["secID","secShortName"]]
df_etffund


# In[ ]:




# In[ ]:

df_future.columns


# In[ ]:

a=mslope(day2week(fuquan(df0)))
Macd_strategy(day2week(fuquan(df0)))
t=Macd_strategy(fuquan(df)).tradeDate.tolist()
y=Macd_strategy(fuquan(df)).equity_curve.values
sinplot("a","b","c","d",t,y)


# In[ ]:


# ===对资金曲线从收益角度进行评价
# 总收益
a=Macd_strategy(fuquan(df))
total_return = (a.iloc[-1]['equity_curve'] / 1) - 1
print '累计收益（%）：', round(total_return * 100, 2)

# 年华收益
# pow(x, y),计算x的y次方
# 年华收益：pow((1 + x), 年数) = 总收益
# 日化收益：pow((1 + x), 天数) = 总收益
# pow((1 + 日化收益), 365) = 年华收益
# 整理得到：年华收益 = pow(总收益, 365/天数) - 1
trading_days = (a['tradeDate'].iloc[-1]-a['tradeDate'].iloc[0]).days + 1
annual_return = pow(total_return, 365.0/trading_days) - 1
print '年华收益（%）：', round(annual_return * 100, 2)

# ===对资金曲线从风险角度进行评价
# 使用每日收益的方差衡量风险
#print '波动率(%)：',round(strategy['chgPct'].std()*100,2)

# 使用最大回撤衡量风险
# 最大回撤：从某一个高点，到之后的某个低点，之间最大的下跌幅度。实际意义：在最最坏的情况下，会亏多少钱。
# 计算当日之前的资金曲线的最高点
a['max2here'] =a['equity_curve'].expanding().max()
# 计算到历史最高值到当日的跌幅，drowdwon
a['dd2here'] = a['equity_curve'] / a['max2here'] - 1
# 计算最大回撤，以及最大回撤结束时间
end_date, max_draw_down = tuple(a.sort_values(by=['dd2here']).iloc[0][['tradeDate', 'dd2here']])
print '最大回撤（%）：', round(max_draw_down * 100, 2)
# 计算最大回撤开始时间
start_date = a[a['tradeDate'] <= end_date].sort_values(by='equity_curve', ascending=False).iloc[0]['tradeDate']
print '最大回撤开始时间', start_date.date()
print '最大回撤结束时间', end_date.date()


# ===终极指标
# 如果只用一个指标来衡量策略，我最常用的就是：年化收益 / abs(最大回撤)
# 越高越好，一般这个指标大于1，说明这个策略值得进一步探索。

    


# In[ ]:

#大小周期结合
week_df0=mslope(day2week(fuquan(df0))) 
df01=mslope(fuquan(df0))
df01=df01[["tradeDate","secID","signal","closePrice"]]
week_df0=week_df0[["tradeDate","signal"]]
strategy = pd.merge(df01, right=week_df0, on=['tradeDate'],how='left', sort=True,suffixes=["_Day","_Week"])
 #
strategy['pos_Week'] = strategy['signal_Week'].shift()
strategy['pos_Week'].fillna(method='ffill', inplace=True)
strategy['chgPct']=strategy["closePrice"].pct_change()
strategy['equity_change_Week'] = strategy['chgPct'] * strategy['pos_Week']
# 根据每天的涨幅计算资金曲线
strategy['equity_curve_Week'] = (strategy['equity_change_Week'] + 1).cumprod()

strategy['pos_Day'] = strategy['signal_Day'].shift()
strategy['pos_Day'].fillna(method='ffill', inplace=True)
strategy['chgPct']=strategy["closePrice"].pct_change()
strategy['equity_change_Day'] = strategy['chgPct'] * strategy['pos_Day']
# 根据每天的涨幅计算资金曲线
strategy['equity_curve_Day'] = (strategy['equity_change_Day'] + 1).cumprod()
strategy[['tradeDate','pos_Week','pos_Day',"equity_curve_Week",'equity_curve_Day']]


#condition1=(strategy["signal_Week"]==1)
#condition2=(strategy["signal_Day"]==0)
#strategy.loc[(condition1),"signal"]=1
#strategy.loc[(condition2),"signal"]=0
#strategy['pos'] = strategy['signal'].shift()
#strategy['pos'].fillna(method='ffill', inplace=True)
#strategy['chgPct']=strategy["closePrice"].pct_change()
#strategy['equity_change'] = strategy['chgPct'] * strategy['pos']
# 根据每天的涨幅计算资金曲线
#strategy['equity_curve'] = (strategy['equity_change'] + 1).cumprod()
strategy.to_csv("do/cesh1.csv")


# In[ ]:

 


# In[ ]:

#加入止损线（均线止损/ATR止损/2%-6%止损）
# ===对资金曲线从收益角度进行评价
# 总收益
total_return = (strategy.iloc[-1]['equity_curve_Week'] / 1) - 1
print '累计收益（%）：', round(total_return * 100, 2)

# 年华收益
# pow(x, y),计算x的y次方
# 年华收益：pow((1 + x), 年数) = 总收益
# 日化收益：pow((1 + x), 天数) = 总收益
# pow((1 + 日化收益), 365) = 年华收益
# 整理得到：年华收益 = pow(总收益, 365/天数) - 1
trading_days = (strategy['tradeDate'].iloc[-1] -  strategy['tradeDate'].iloc[0]).days + 1
annual_return = pow(total_return, 365.0/trading_days) - 1
print '年华收益（%）：', round(annual_return * 100, 2)

# ===对资金曲线从风险角度进行评价
# 使用每日收益的方差衡量风险
print '波动率(%)：',round(strategy['chgPct'].std()*100,2)

# 使用最大回撤衡量风险
# 最大回撤：从某一个高点，到之后的某个低点，之间最大的下跌幅度。实际意义：在最最坏的情况下，会亏多少钱。
# 计算当日之前的资金曲线的最高点
strategy['max2here'] = strategy['equity_curve_Week'].expanding().max()
# 计算到历史最高值到当日的跌幅，drowdwon
strategy['dd2here'] = strategy['equity_curve_Week'] / strategy['max2here'] - 1
# 计算最大回撤，以及最大回撤结束时间
end_date, max_draw_down = tuple(strategy.sort_values(by=['dd2here']).iloc[0][['tradeDate', 'dd2here']])
print '最大回撤（%）：', round(max_draw_down * 100, 2)
# 计算最大回撤开始时间
start_date = strategy[strategy['tradeDate'] <= end_date].sort_values(by='equity_curve_Week', ascending=False).iloc[0]['tradeDate']
print '最大回撤开始时间', start_date.date()
print '最大回撤结束时间', end_date.date()


# ===终极指标
# 如果只用一个指标来衡量策略，我最常用的就是：年化收益 / abs(最大回撤)
# 越高越好，一般这个指标大于1，说明这个策略值得进一步探索。





# In[ ]:

"""
# ===对每次操作的评价
# 平均涨幅
print '平均涨幅（%）', round(select_stock['下月平均涨跌幅'].mean() * 100, 2)

# 胜率
print '涨幅>0比例（%）', select_stock[select_stock['下月平均涨跌幅'] > 0].shape[0] / float(select_stock.shape[0]) * 100

# 胜率
print '跑赢同期均值比例（%）', select_stock[select_stock['下月平均涨跌幅'] > select_stock['所有股票下月平均涨跌幅']].shape[0] / float(select_stock.shape[0]) * 100

# 最大单月涨幅，最大单月跌幅
print '最大单月涨幅（%）：', round(select_stock['下月平均涨跌幅'].max() * 100, 2)
print '最大单月跌幅（%）：', round(select_stock['下月平均涨跌幅'].min() * 100, 2)  # 单月最大下跌30%，是否还有信心坚持策略？
"""

