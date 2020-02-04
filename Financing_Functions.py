import os
import pandas as pd

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
    print('DONE')
    return df