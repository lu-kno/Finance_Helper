from datetime import datetime, timedelta

class C_Transaction():
    def __init__(self, theline):
        self.date=''
        self.type=''
        self.info=''
        self.amount=''
        self.category='Undefined'

        self.date=datetime.strptime(theline[:theline.find(';')], '%d.%m.%Y')
        theline=theline[theline.find(';')+1:]
        theline=theline[theline.find(';')+1:]

        self.type=theline[:theline.find(';')]
        theline=theline[theline.find(';')+1+1:]

        self.info=theline[:theline.find('"')-1]
        theline=theline[theline.find('"')+1+1:]

        self.amount=float(theline[:theline.find(';')].replace(',','.'))

        categories={'SUPER':    ['REWE','YORMAS','EDEKA','Netto','DM-Drogerie','Rossmann','Feneberg','Lidl'],
                    'FOOD':     ['GIANOLI','McDonald', 'Burger King'],
                    'CONSTANT': ['Telefonica','Patreon','Techniker Krankenkasse','Miete','Spotify'],
                    'TRANSPORT':['comuto','DBVERTRIEB','FlixBus','RVV-TICKETAUTOMAT'],
                    'FUN':      ['BLIZZARD','LYNEX', 'Curiosityst', 'EUROBILL', 'Galeria','Bitpanda'],
                    'CLOTHING': ['MOUNTAIN WAREHOUSE','H+M','TK MAXX'],
                    'AMAZON':   ['AMAZON'],
                    'CASH':     ['Auszahlung'],
                    'GIFTS':    ['Xmas', 'Savings'],
                    'INCOME':   ['Continental','Staatsoberkasse Bayern','Christian Knoblich','Zinsen'],
                    'OTHERS':   ['SHELL','AU Consulting GmbH','TOOM','KAMERA EXPRESS'],
                    'Amsterdam':['ALMERE','Nes Supermarket','HEXOBS','MOCO Museum','L.S. Domino','SHELTER','KIOSK WESTTunnel', 'AMSTERDAM', 'Tulip House', 'RA Tickets','ETOS', 'KEOLIS']
                    }

        found = 0
        for category in categories.keys():
            for info in categories[category]:
                if info.upper() in self.info.upper():
                    self.info = info
                    self.category = category
                    found = 1
                    break
            if found == 1 : break
        
        if 'PayPal (Europe)' in self.info: 
            self.info=self.info[self.info.find(' . ')+3:]
            tmp=self.info[:self.info.find(',')]
            self.info=tmp.strip()

        if self.category=='Undefined': self.category=self.info


def GetExpenses(thething, start, end, info=None, exinfo=None, name=None):
    print('from: ', start)
    print('until: ', end)
    total=0
    for i in thething:
        if start<i.date<end: ## i might just need to write start and end, depending on how i implement the .date method when calling the function
            if info is None and exinfo is None: total=total+i.amount
            elif info is not None and exinfo is None:
               if i.info in info: total=total+i.amount
            elif info is None and exinfo is not None: 
                if i.info not in exinfo: total=total+i.amount
    if name is not None:
        print(name, ': ', total)
        return
    print(info,'~',exinfo,'~','=',total)
    return

def GetExpensesByCategory(thething, start, end):
    print('from: ', start)
    print('until: ', end)
    total=0
    thedict=dict()
    for i in thething:
        if start<i.date<end:
            if i.category in thedict.keys(): thedict[i.category]=thedict[i.category]+i.amount
            else: thedict[i.category]=i.amount
    for i in thedict.keys():
        print(thedict[i], '\t=\t', i)

def GetExpensesByInfo(thething, start, end):
    print('from: ', start)
    print('until: ', end)
    total=0
    thedict=dict()
    for i in thething:
        if start<i.date<end:
            if i.info in thedict.keys(): thedict[i.info]=thedict[i.info]+i.amount
            else: thedict[i.info]=i.amount
    for i in thedict.keys():
        print(thedict[i], '\t=\t', i)