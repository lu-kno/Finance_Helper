import os
import pickle
import pandas
from datetime import datetime, timedelta
from Financing_Functions import *

filename= 'Umsaetze_feb2020'

df=get_data(filename)
#df=parse_descriptions(df, categories_dict)
df=parse_categories(df, categories_dict)
daily_in, daily_out=plot_pie(df, colormap='tab20')

#tmp=df.loc[df.loc[:,'Category']=='Uncategorized',['Description','Amount']]