import os
import re
import json
import pandas as pd
import matplotlib.pyplot as plt
from categories import categories_dict, category_color

from config import * # containing the path where the files csv and pkl are saved


pklName='UmsatzLog'


def get_data(*files,workspace=workspace, file_path=file_path, from_original=1, parse=0):
    print('Getting Data...')
    pkl=0
    csv=0
    pklpath=workspace+pklName+'.pkl'
    

    # all files from 'file_path' will be parsed, together with the ones from argument *files
    available_files=os.listdir(file_path)
    try:
        with open(workspace+'parsed_files.json') as file: parsed_files=json.load(file)
    except:
        parsed_files=[]
    to_parse=[p for p in available_files if p not in parsed_files]


    files=list(files)+to_parse
    cols=['Book_Date',
            'Pay_Date',
            'Type',
            'Book_Text',
            'Amount',
            'Currency',
            'Auftraggeberkonto',
            'BLZ_Auftraggeberkonto',
            'IBAN_Auftraggeberkonto',
            'Category']

    if os.path.isfile(pklpath): 
        df_pkl=pd.read_pickle(pklpath)
        pkl=1
    else:
        pkl=0
        df_pkl=pd.DataFrame(columns=cols)

    if len(files)>0:
        for file in files:
            csvpath=workspace+file
            if not file.endswith('.CSV'): csvpath=csvpath+'.CSV'

            csv=1
            df = pd.read_csv(csvpath, sep =';', header=0, names=cols, index_col=False, decimal=',',
                                dayfirst=True, infer_datetime_format=True, parse_dates=['Book_Date', 'Pay_Date'])
        
            df=df.fillna(value=0)
            df=parse_categories(df,categories_dict)
            df=df[df['Book_Date'].apply(type)!=type(0)]  # ignore if no Transaction date is given in the CSV
            df['Book_Date']=df['Book_Date'].apply(lambda BD: BD.to_datetime64())
            df=get_hash(df)
            df=df.drop(columns=['Pay_Date', 'Auftraggeberkonto', 'BLZ_Auftraggeberkonto', 'IBAN_Auftraggeberkonto'])
    
            endDatePKL=max(df_pkl['Book_Date'])
            #df_pkl=df_pkl.drop(labels=df_pkl.loc[df_pkl['Book_Date']>=endDatePKL].index)
            df_pkl=df_pkl[df_pkl['Book_Date']<endDatePKL]
            df=df[df['Book_Date']>=endDatePKL]
            df_merged=pd.merge(df,df_pkl,how='outer')
            df_pkl=df_merged
        parsed_files=list(parsed_files)+list(to_parse)
        with open(workspace+'parsed_files.json','w+') as file: json.dump(parsed_files,file)

    if parse: df_pkl=parse_categories(df_pkl,categories_dict)
    save_pkl(df_pkl)
    print('DONE')

    return df_pkl

def get_hash(dataframe):
    print('Getting HASH...')
    df=dataframe
    toHash=df['Book_Date'].apply(str)+df['Book_Text'].apply(str)+df['Amount'].apply(str)
    df['HASH']=toHash.apply(hash)
    print('DONE')
    return df

def find_category(description,dictionary):
    for cat, patterns in dictionary.items():
        for pattern in patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return cat, match.group()
    return  'Undefined','Unknown'

def parse_categories(dataframe,category_dict):
    print('Parsing Categories...')
    df=dataframe
    found_categories=df['Book_Text'].apply(find_category, args=[category_dict])
    df['Category'], df['Description']= zip(*found_categories)
    print('DONE')
    return df

def plot_pie(dataframe, group_by='Category', colormap='tab20'):   #colormap='hsv'
    '''A pie plot is created with the data grouped by category as default.'''
    print('Plotting Data Pie...')
    df=dataframe
    ax = plt.gca()
    # pie chart with expenses separated by categories
    df_group_sum=df.groupby(by=group_by).sum()
    df_expenses_cat=df_group_sum.loc[df_group_sum.loc[:,'Amount']<=0,:].abs().drop(labels=['CONSTANT',])#'TEMPORARY'
    explode=[0.05 for i in df_expenses_cat.index.tolist()]
    df_expenses_cat.plot.pie(y='Amount', 
                             #table=df_expenses_cat, 
                             explode=explode, 
                             cmap=colormap, 
                             ax=ax, 
                             title='Expenses by '+group_by, 
                             autopct=make_autopct(df_expenses_cat.loc[:,'Amount']))# labels=df_expenses_cat.index,   '%2.1f%%'
    #plt.title("expenses")
    plt.legend(loc='upper right')
    plt.show()
    print('DONE')
    return

#fig, axes = plt.subplots(nrows=3, ncols=4)
def plot_more_pies(dataframe, group_by='Category', colormap='tab20',dates=[],width=1):   #colormap='hsv'
    '''This is a variation of the 'plot_pies' function, which creates a grid of subplots for each group from the function 'plot_monthly_pies'.
    This function is meant to be applied to groups of a dataframe in the aforementioned function.
    For each group, a pie plot is created with the data separated by category'''
    print('Plotting Data Pie...')
    global axes
    global plotnr
    global category_color
    df=dataframe
    if dates: date=str(dates[plotnr][0])+', '+str(dates[plotnr][1])
    else: date='not specified'

    #ax = plt.gca()
    # pie chart with expenses separated by categories
    df_group_sum=df.groupby(by=group_by).sum()
    df_expenses_cat=df_group_sum.loc[df_group_sum.loc[:,'Amount']<=0,:].abs().drop(labels=['CONSTANT',])#'TEMPORARY'
    
    ## This two lines are for coor coding each cateory did not work
    #colormaps=[category_color[cat] for cat in list(df_expenses_cat.index)]
    #colormap = cm.get_cmap(colormap)

    explode=[0.05 for i in df_expenses_cat.index.tolist()]
    pie_wedge_collection = df_expenses_cat.plot.pie(y='Amount', 
                             #table=df_expenses_cat, 
                             explode=explode, 
                             legend=False, 
                             #cmap=colormap, 
                             #ax=axes[plotnr//4,plotnr%4], # Uses number of months
                             ax=axes[plotnr//width,plotnr%width],  # Uses grid_guide from number of months
                             #ax=axes[0,0],
                             title='Expenses from ' + date, 
                             autopct=make_autopct(df_expenses_cat.loc[:,'Amount']),
                             #colors=colormaps
                             )# labels=df_expenses_cat.index,   '%2.1f%%'

    ## For color coding each category
    #for pie_wedge in pie_wedge_collection:
    #    pie_wedge.set_edgecolor('white')
    #    pie_wedge.set_facecolor(category_dict[pie_wedge.get_label()])

    #plt.title("expenses")
    #plt.legend(loc='upper right')
    #plt.show()
    plotnr=plotnr+1
    print('DONE')
    return

def plot_monthly_pies(dataframe):
    '''This function takes in a DataFrame object, groups it by month.
    To each Group the function "plot_more_pies" is applied, creatin a pie plot for each month of data.'''
    global axes
    global fig
    global plotnr
    grid_guide={1:(1,1),
          2:(1,2),
          3:(1,3),
          4:(2,2),
          5:(2,3),
          6:(2,3),
          7:(2,4),
          8:(2,4),
          9:(3,3),
          10:(3,4),
          11:(3,4),
          12:(3,4),
          13:(3,5),
          14:(3,5),
          15:(3,5),
        }
    plotnr=0
    df=dataframe
    df.index=df['Book_Date']
    df=df.groupby(by=[ df.index.year, df.index.month,])
    groups=list(df.groups.keys())
    grid=grid_guide[len(groups)]
    print(len(groups))
    #fig, axes = plt.subplots(nrows=(len(groups)-1)//4+1, ncols=4)       # Uses number of months
    fig, axes = plt.subplots(nrows=grid[0], ncols=grid[1])       # Uses grid_guide from number of months
    print(axes)
    #df.apply(plot_more_pies, dates=groups)       # Uses number of months
    df.apply(plot_more_pies, dates=groups,width=grid[1])       # Uses grid_guide from number of months
    plt.show()

def plot_bar(dataframe, colormap='tab20'):
    df=dataframe
    # Bar chart with daily expenses and incomes
    #df_daily=pd.DataFrame(columns=['INCOME','EXPENSES'])
    df_daily_income=df.loc[df.loc[:,'Amount']>0,:].groupby('Book_Date').sum().rename(columns={'Amount': 'IN'}).loc[:,['IN']]
    df_daily_expenses=df.loc[df.loc[:,'Amount']<0,:].groupby('Book_Date').sum().rename(columns={'Amount': 'OUT'}).loc[:,['OUT']]
    df_daily=pd.merge(df_daily_income,df_daily_expenses,how='outer', left_index=True, right_index=True)
    df_daily.plot.bar(subplots=False, title='Daily Transactions',width=1.0)
    #plt.title("expenses")
    plt.legend(loc='upper right')
    plt.show()
    print('DONE')
    return
       
def get_dates(dataframe, from_='', until_=''):
    '''This function takes in a pandas.DataFrame object with a date column 'Book_Date', 
    and returns another dataframe without the unneeded data'''
    print('Getting Dates...')
    df=dataframe
    if from_ is not '': 
        print('From: %s' % from_)
        df=df.loc[df.loc[:,'Book_Date']>=from_,:]
    if until_ is not '': 
        print('Until: %s' % until_)
        df=df.loc[df.loc[:,'Book_Date']<=until_,:]
    print('DONE')
    return df

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}% ({v:d})'.format(p=pct,v=val)
    return my_autopct

def save_pkl(df):
    df.to_pickle(workspace+pklName+'.pkl')
    return