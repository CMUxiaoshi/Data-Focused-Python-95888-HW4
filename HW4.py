#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 17:22:45 2022

@author: sx
"""

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from datetime import datetime
import matplotlib.ticker as tk

def open_file(path):
    data=open(path)
    data=data.readlines()
    return data

def drop_n(data):
    dropped_data=[]
    for i in data: 
        dropped_data.append(i.replace('\n','').split(','))
    return dropped_data

def drop_the_first_line(data):
    dropped_data=[data[0]]
    data.pop(0)
    return dropped_data,data

def list_sorted(raw_list):
    data=sorted(raw_list,key=lambda i:i[0])
    return data

def first_step(path):
    
    headline,data=drop_the_first_line(drop_n(open_file(path)))
    sorted_data=list_sorted(data)
    return headline,sorted_data

def type_change(data):
    for i in data:
        for j in range(1,len(i)):
            i[j]=float(i[j])
    return data

def date_change(data):
    date_pri=data[:6]
    date_later=data[8:10]
    date=date_pri+date_later
    return date

def date_change_inlist(data):
    for i in data:
        i[0]=date_change(i[0])
    return data

def dayscalculate(data):
    date_raw=[]
    date_after=[]
    for i in data:
        i[0]=i[0]+'20'
        date_raw.append(datetime.strptime(i[0],'%m/%d/%Y'))
    for j in range(0,len(date_raw)):
        if j==0:
            date_after.append(0)
        else:
            date_after.append(str(date_raw[j]-date_raw[1]))
        
    date_after[1]=1
    for k in range(2,len(date_after)):
        if len(date_after[k])==15:
            date_after[k]=int(date_after[k][0])
        elif len(date_after[k])==16:
            date_after[k]=int(date_after[k][0:2])
        else:
            date_after[k]=int(date_after[k][0:3])
    return date_after


def question_a(path,filename):    
    headline,sorted_data=first_step(path)
    sorted_data=type_change(sorted_data)
    sorted_data=date_change_inlist(sorted_data)
    sorted_data.insert(0,headline)
    output = open(filename,'w+')
    for i in range(len(sorted_data)):
        for j in range(len(sorted_data[i])):
            output.write(str(sorted_data[i][j]))
            output.write(' ') 
        output.write('\n') 
    output.close()
    return sorted_data


def XYZ(sorted_data):
    headline=sorted_data.pop(0)
    headline=headline[0]
    for i in range(len(headline)):
        headline[i]=headline[i].strip('"')
    time_series=list(zip(*sorted_data))
    month=list(zip([1, 2, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360]))
    X=np.array([dayscalculate(sorted_data)])
    Y=np.array(month)
    Z=np.array([i for i in time_series if time_series.index(i)!=0])
    return X,Y,Z,headline

def picture_3d(X,Y,Z):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.set_xlabel('trading days since 01/02/20')
    ax.set_ylabel('months to maturity')
    ax.set_zlabel('rate')
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    x_major=tk.MultipleLocator(50)
    y_major=tk.MultipleLocator(50)
    z_major=tk.MultipleLocator(0.5)
    ax.xaxis.set_major_locator(x_major)
    ax.yaxis.set_major_locator(y_major)
    ax.zaxis.set_major_locator(z_major) 
    plt.show()

def picture_wire(X,Y,Z):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
    ax.set_xlabel('trading days since 01/02/20')
    ax.set_ylabel('months to maturity')
    ax.set_zlabel('rate')
    plt.show()

def interest_Rate_timeseries(data,headline):
    yield_curve_df=pd.DataFrame(data,index=list(zip(*data))[0],columns=headline)
    yield_curve_df.plot()
    plt.title('Interest Rate Time Series, 2020')
    plt.legend(loc="upper right",prop={'size': 6}) 
    plt.show()
    return yield_curve_df
    
def by_day_yield_curve(data,X):
    by_day_yield_curve_df=data.transpose()
    by_day_yield_curve_df.columns=[i for i in X]
    date_count=[i for i in range(0,260,20)]
    days=[]
    for day in date_count:
        days.append(X[0][day])
    test=by_day_yield_curve_df.loc[:,days]
    test.columns=list(test.loc['Date'])
    test=test.drop(labels='Date')
    test.index=[1, 2, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360]
    test.plot()
    plt.title('2020 Yield Curves,20 Day Intervals')
    plt.legend(loc="lower right",prop={'size': 6}) 
    plt.show()

def main():
#path
    data2019=question_a('/Users/sx/Desktop/Carnegie Mellon University/data focused python/HW4/daily-treasury-rates.csv','daily_yield_curves_2019.txt')
    data2020=question_a('/Users/sx/Desktop/Carnegie Mellon University/data focused python/HW4/daily-treasury-rates 2.csv','daily_yield_curves_2020.txt')
    X,Y,Z,headline=XYZ(data2020)
    #surface plots
    picture_3d(X,Y,Z)
    #wireframe plots
    picture_wire(X,Y,Z)
    #interest_rate_timeseries
    yield_curve_df=interest_Rate_timeseries(data2020, headline)
    #by day yield curve
    by_day_yield_curve(yield_curve_df,X)


if __name__=='__main__':
    main()