import os
import pandas as pd
import matplotlib as plt

def get_data(name,workspace=r'C:\Users\chris\Documents\Unimportant\\', from_original=0):
    print('Getting Data...')
    csvpath=workspace+name+'.CSV'
    pklpath=workspace+name+'.pkl'

    cols=['Book_Date',
          'Pay_Date',
          'Type',
          'Description',
          'Amount',
          'Currency',
          'Auftraggeberkonto',
          'BLZ_Auftraggeberkonto',
          'IBAN Auftraggeberkonto',
          'Category']

    if not os.path.isfile(pklpath) or from_original:
        df = pd.read_csv(csvpath, sep =';', header=0, names=cols, index_col=False, decimal=',',
                         dayfirst=True, infer_datetime_format=True, parse_dates=['Book_Date', 'Pay_Date'])
    else: df = pd.read_pickle(pklpath)
    df=df.fillna(value=0)
    df=df.drop(columns=['Pay_Date', 'Auftraggeberkonto', 'BLZ_Auftraggeberkonto', 'IBAN Auftraggeberkonto'])
    print('DONE')
    return df

def parse_descriptions(dataframe, keywords):
    print('Parsing Descriptions...')
    df=dataframe
    for key in keywords:
        df.loc[df['Description'].contains(key), 'Description']=key
    print('DONE')
    return df
        
def parse_categories(dataframe, categories_dict):
    print('Parsing Categories...')
    df=dataframe
    for group in categories_dict.keys():
        df.loc[df['Description'].isin(categories_dict[group]), 'Category'] = group
    print('DONE')
    return df

def plot_pie(dataframe, group_by='Category', colormap='hsv'):
    df_group_sum=dataframe.group_by(by=group_by).sum()
    df_group_sum.plot.pie(y='Amount', cmap=colormap, labels=df.index())
       
