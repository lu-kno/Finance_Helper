import os
import pickle
import pandas as pd
import tkinter as tk
from tkinter import *
from datetime import datetime, timedelta
import calendar
from Financing_Functions import *
from categories import categories_dict

df=0
def importCSV():
    df=get_data(*file_paths)
    return

def printVars():
    print(strtDayVar.get(),strtMonthVar.get(),strtYearVar.get())
    print(endDayVar.get(),endMonthVar.get(),endYearVar.get())

def plotData():
    #set first day of year if no month is given
    if not strtMonthVar.get():      
        strtMonthVar.set('1')
        strtDayVar.set('1')
    #set first day of month if no day is given
    elif not strtDayVar.get():      
        strtDayVar.set('1')
    #fix months with less than 31 days
    elif strtDayVar.get()=='31':    
        strtDayVar.set( str(calstrtar.monthrange( int(strtYearVar.get()), int(strtMonthVar.get()) )[1]) )
    from_=strtYearVar.get()+'-'+strtMonthVar.get()+'-'+strtDayVar.get()

    #set last day of year if no month is given
    if not endMonthVar.get():               
        endMonthVar.set('12')
        endDayVar.set('31')
    #set last day of month if no day is given #fix months with less than 31 days
    elif not endDayVar.get() or endDayVar.get()=='31':          
        endDayVar.set( str(calendar.monthrange( int(endYearVar.get()), int(endMonthVar.get()) )[1]) )
    until_=endYearVar.get()+'-'+endMonthVar.get()+'-'+endDayVar.get()

    print(from_)
    print(until_)
    df=get_data(parse=1)
    df=get_dates(df,from_=from_,until_=until_)
    plot_pie(df)

def plotMonth():
    from_=theYearVar.get()+'-'+theMonthVar.get()+'-'+'1'
    until_=theYearVar.get()+'-'+theMonthVar.get()+'-'+str(calendar.monthrange( int(theYearVar.get()), int(theMonthVar.get()) )[1])

    print(from_)
    print(until_)
    df=get_data(parse=1)
    df=get_dates(df,from_=from_,until_=until_)
    plot_pie(df)

def plotPies():
    df=get_data()
    plot_pies(df)

root=tk.Tk(className='Finance Overview')
topframe=Frame(root).grid(row=0, column=0)
bottomFrame=Frame(root).grid(row=1, column=0)
monthFrame=Frame(root).grid(row=2, column=0)

strtDayVar=StringVar(root)
strtMonthVar=StringVar(root)
strtYearVar=StringVar(root)

endDayVar=StringVar(root)
endMonthVar=StringVar(root)
endYearVar=StringVar(root)

day=Label(bottomFrame,text='Day').grid(row=0, column=3)
month=Label(bottomFrame,text='Month').grid(row=0, column=2)
year=Label(bottomFrame,text='Year').grid(row=0, column=1)

start=Label(bottomFrame,text='Start').grid(row=1, column=0)
strtDay=OptionMenu(bottomFrame,strtDayVar,*[x+1 for x in range(31)]).grid(row=1, column=3)
strtMonth=OptionMenu(bottomFrame,strtMonthVar,*[x+1 for x in range(12)]).grid(row=1, column=2)
strtYear=OptionMenu(bottomFrame,strtYearVar,*[2018,2019,2020,2021]).grid(row=1, column=1)

end=Label(bottomFrame,text='End').grid(row=2, column=0)
endDay=OptionMenu(bottomFrame,endDayVar,*[x+1 for x in range(31)]).grid(row=2, column=3)
endMonth=OptionMenu(bottomFrame,endMonthVar,*[x+1 for x in range(12)]).grid(row=2, column=2)
endYear=OptionMenu(bottomFrame,endYearVar,*[2018,2019,2020,2021]).grid(row=2, column=1)

printButton=Button(bottomFrame, text="plot selection",activebackground='red', activeforeground='white', command=plotData, bg='snow3', width=15).grid(row=0,column=0)

#########################################
day=Label(monthFrame,text='Year').grid(row=3, column=1)
day=Label(monthFrame,text='Month').grid(row=3, column=2)

theMonthVar=StringVar(root)
theYearVar=StringVar(root)

theYear=OptionMenu(monthFrame,theYearVar,*[2018,2019,2020]).grid(row=4, column=1)
theMonth=OptionMenu(monthFrame,theMonthVar,*[x+1 for x in range(12)]).grid(row=4, column=2)

printButton=Button(monthFrame, text="plot month",activebackground='red', activeforeground='white', command=plotMonth, bg='snow3', width=15).grid(row=3,column=0)



root.mainloop()