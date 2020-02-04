import os
import pickle
import pandas
from datetime import datetime, timedelta
from FunctionsClasses import *

filename= 'umsatze.CSV'



CSV_FilePath='C:/Users/Christian/Documents/Unimportant/'+filename
with open(CSV_FilePath, 'r') as file:
    lines=file.readlines()

thing=[]
first=True
for line in lines:
    if first: first=False
    elif line=='\n' or line=='': pass
    else: 
        transaction=C_Transaction(line)
        thing.append(transaction)

end=datetime.now()
start=end-timedelta(days=18)


keywords=['REWE',
            'Techniker Krankenkasse',
            'AMAZON',
            'Telefonica',
            'RVV-TICKETAUTOMAT',
            'MCDONALDS',
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
            'TOOM'
            ]

super=['REWE',
        'YORMAS',
        'EDEKA',
        'Netto',
        'DM-Drogerie',
        'Feneberg'
        ]

#for i in keywords:
#    GetExpenses(thing, start, end, info=i)

    
#print('TOTAL KNOWN')
#GetExpenses(thing, start, end, info=keywords)


#print('TOTAL')
#GetExpenses(thing, start, end, exinfo=keywords, name='others')

GetExpensesByCategory(thing, start, datetime.now())



#GetExpensesByInfo(thing, start, end)