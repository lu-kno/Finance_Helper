import os
import pickle
import pandas as pd
from datetime import datetime, timedelta
from Financing_Functions import *
from categories import categories_dict


files=[
    'umsaetze2019Dec',
    'umsaetze2020Feb',
    'Umsaetze_feb2020',
    ]
filename= files[1]
plot=0

df0=get_data(parse=1)#'Umsaetze_KtoNr144701000_EUR_14-03-2020_1907'
#df=parse_categories(df, categories_dict)
df=get_dates(df0,from_='2019-12',until_='2020-04')
#df.index=df['Book_Date']
#dff=df.groupby(by=[df.index.month, df.index.year])
plot_monthly_pies(df)
if plot: plot_pie(df, colormap='tab20')
#tmp=df.loc[df.loc[:,'Category']=='Uncategorized',['Description','Amount']]