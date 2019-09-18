import numpy as np
import pandas as pd
import matplotlib as mp
import matplotlib.pyplot as plt
import pytz 
import datetime
from tzlocal import get_localzone


dates= pd.date_range('20150101', '20150201',freq='5D',tz=get_localzone())
'''print dates'''
df=pd.DataFrame(np.random.randn(7,4), index = dates, columns=list('ABCD'))
'''print df'''

k = list(range(4))
'''print k'''
k = np.array([4]*4)
'''print k'''

temo=[pd.Timestamp('20180101'),pd.Timestamp('20180102'),pd.Timestamp('20180103'),pd.Timestamp('20180104')]
df2= pd.DataFrame({'A':3, 'B':temo,'C':pd.Series(1.6,index=list(range(0,8,2))), 'D':[3]+[5]+[7]+[9], 'E':'Hi'})
'''print df2[2:][df2['D']>df2['A'].mean()+1]'''
'''print '20180102' in df2 '''
print df2
'''bool_vec=[True,False,False,True]
bool_vev=[True,True,False,False,False]
print df2[['A','C']].loc[[0,4]]
print df2.loc[[0,4]][['A','C']]
print df2['A'][2]
print df2.iloc[0][2]'''

'''pt=df2[df2['A']==3].set_index('B')['D']
pt.plot(title="Test here")
plt.show()'''

'''df_grp=df2.groupby('B')
grp_mean=df_grp.mean()
print grp_mean'''

df3=df2.sort_values(by='B',ascending=False)
print df3