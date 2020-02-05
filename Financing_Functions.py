import os
import pandas as pd
import matplotlib.pyplot as plt

keywords=[
        'REWE',
        'Techniker Krankenkasse',
        'AMAZON',
        'Telefonica',
        'RVV-TICKETAUTOMAT',
        'MCDONALD',
        'Burger King',
        'Bitpanda',
        'YORMAS',
        'EDEKA',
        'Auszahlung',
        'MOUNTAIN WAREHOUSE',
        'Netto',
        'SHELL',
        'DBVERTRIEBG',
        'DM-Drogerie',
        'Feneberg',
        'Patreon',
        'AU Consulting GmbH',
        'TOOM',
        'ALDI',
        'Lidl',
        'PENNY',
        'COMUTO',
        'FRISTO',
        'SPOTIFY',
        'Apotheke',
        'STEAM GAMES',
        'HSK MENSA',
        'M(ü|ue|u)ller'
        ]

categories_dict={
                'SUPER':    ['REWE','YORMAS','FRISTO','EDEKA','Netto','PENNY','DM(-Drogerie|)','M(ü|ue|u)ller','Rossmann','Feneberg','real GmbH','Lidl', 'ALDI', 'Apotheke', 'Kunkel OHG'],
                'FOOD':     ['GIANOLI','Mc( |)Donald', 'Burger King', 'CHIPOTLE MEXICAN GRILL', 'HSK MENSA', 'TAKEAWAYCOM', 'WONDER WAFFEL', 'NORDSEE GmbH', 'Rooster Fried Chicken'],
                'CONSTANT': ['Telefonica','Patreon','Techniker Krankenkasse','Miete','Spotify'],
                'TRANSPORT':['COMUTO','DBVERTRIEB','FlixBus','RVV-TICKETAUTOMAT'],
                'FUN':      ['BLIZZARD','LYNEX', 'Curiosityst', 'EUROBILL', 'Galeria','Bitpanda', 'LOVOO', 'STEAM GAMES', 'Fellhornbahn', 'GOOGLE', 'MINECRAFT'],
                'CLOTHING': ['MOUNTAIN WAREHOUSE','H\+M','TK MAXX', 'NEW YORKER', 'Bijou Brigitte', 'Hopfer \+ Hopfer', 'Woolworth'],
                'AMAZON':   ['AMAZON'],
                'CASH':     ['Auszahlung', 'EINZAHLUNG'],
                'GIFTS':    ['Xmas'],
                'SAVINGS':  ['Savings'],
                'INCOME':   ['Continental','Staatsoberkasse Bayern','Christian Knoblich','Zinsen', 'Muesli LOHN / GEHALT'],
                'OTHERS':   ['SHELL','AU Consulting GmbH','TOOM','KAMERA EXPRESS', 'Johanniter-Unfall-Hilfe e.V.', 'Action 3131', 'PURNATUR', 'UNICEF'],
                'TRAVEL':   ['AirBnB', 'LUFTHAN(|SA)', 'Camping 3 Estrellas', 'AEROP ADOLFO SUAREZ M', 'taxi'],
                'Amsterdam':['ALMERE','Nes Supermarket','HEXOBS','MOCO Museum','L.S. Domino','SHELTER','KIOSK WESTTunnel', 'AMSTERDAM', 'Tulip House', 'RA Tickets','ETOS', 'KEOLIS']
                }

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
    df.loc[:,'Category']='Uncategorized'
    df['Keyword']=''
    df=df.drop(columns=['Pay_Date', 'Auftraggeberkonto', 'BLZ_Auftraggeberkonto', 'IBAN Auftraggeberkonto'])
    print('DONE')
    return df

def parse_descriptions(dataframe, categories_dict):
    print('Parsing Descriptions...')
    df = dataframe
    keywords = [ i for n in categories_dict.keys() for i in categories_dict[n] ]
    for key in keywords:
        df.loc[df.loc[:,'Description'].str.contains(key, case=False, flags=1), 'Description'] = key.replace('\\','')
    print('DONE')
    return df
        
def parse_categories(dataframe, categories_dict):
    print('Parsing Categories...')
    df=dataframe
    for group in categories_dict.keys():
        df.loc[df.loc[:,'Description'].str.contains('|'.join(categories_dict[group]), case=False, flags=1), 'Category'] = group

        #df.loc[df['Description'].isin(categories_dict[group]), 'Category'] = group
    print('DONE')
    return df

def plot_pie(dataframe, group_by='Category', colormap='hsv'):
    print('Plotting Data...')
    df=dataframe
    ax = plt.gca()
    # pie chart with expenses separated by categories
    df_group_sum=dataframe.groupby(by=group_by).sum()
    df_expenses_cat=df_group_sum.abs().drop('INCOME')
    df_expenses_cat.plot.pie(y='Amount', cmap=colormap, labels=df_group_sum.index, ax=ax, title='Expenses by Category')

    # Bar chart with daily expenses and incomes
    #df_daily=pd.DataFrame(columns=['INCOME','EXPENSES'])
    df_daily_income=df.loc[df.loc[:,'Amount']>0,:].groupby('Book_Date').sum().rename(columns={'Amount': 'IN'})
    df_daily_expenses=df.loc[df.loc[:,'Amount']<0,:].groupby('Book_Date').sum().rename(columns={'Amount': 'OUT'})
    df_daily=pd.merge(df_daily_income,df_daily_expenses,how='outer', left_index=True, right_index=True)
    df_daily.plot.bar(subplots=False, title='Daily Transactions',width=1.0)


        
    plt.title("expenses")
    plt.legend(loc='upper right')
    plt.show()
    print('DONE')
    return df_daily_income, df_daily_expenses
       

df2=parse_descriptions(get_data('umsatze'), categories_dict)
df=parse_categories(df2, categories_dict)
daily_in, daily_out=plot_pie(df, colormap='tab20')

tmp=df.loc[df.loc[:,'Category']=='Uncategorized',['Description','Amount']]