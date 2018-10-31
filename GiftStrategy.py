#-*-coding:utf-8 -*-
import requests
import urllib2 as url
import random
import json
from time import sleep
import numpy as np
import pandas as pd
import chardet
import string
import sys 
import re
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta

reload(sys)                      # reload 才能调用 setdefaultencoding 方法  
sys.setdefaultencoding('utf-8')  # 设置 'utf-8' 

    
def DownloadData():
    date = '2018-10-30'
    variety_sh = ['rb1901','ru1901','ni1901','bu1812','hc1901']
    variety_SH = ['RB', 'RU', 'NI','BU','HC']
    mkt_sh = '069001005'
    outname = 'report_'+date+'.txt'
    f = open(outname,'w')    
    for i in range(len(variety_SH)):
        resp = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=QHCC&sty=QHSYCC&stat=3&fd='+ date +'&mkt='+ mkt_sh +'&code='+ variety_sh[i] +'&sc='+ variety_SH[i] +'&cb=callback&callback=callback&_=1540896735401'
        f.write(variety_sh[i]+'\n')
        data_list = ProcessData(resp)
        AnalysisList(f,data_list)
    ##dalian
    variety_dl = ['i1901','j1901','jm1901','jd1901','m1901','v1901']
    variety_DL = ['I','J','JM','JD','M','V']
    mkt_dl = '069001007'
    for i in range(len(variety_DL)):
        resp = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=QHCC&sty=QHSYCC&stat=3&fd='+ date +'&mkt='+ mkt_dl +'&code='+ variety_dl[i] +'&sc='+ variety_DL[i] +'&cb=callback&callback=callback&_=1540896735401'
        f.write(variety_dl[i]+'\n')
        data_list = ProcessData(resp)
        AnalysisList(f,data_list)
    ##zhenzhou
    variety_zz = ['zc1901','sr1901','rm1901','ma1901']
    variety_ZZ = ['ZC','SR','RM','MA']
    mkt_zz = '069001008'
    for i in range(len(variety_ZZ)):
        resp = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=QHCC&sty=QHSYCC&stat=3&fd='+ date +'&mkt='+ mkt_zz +'&code='+ variety_zz[i] +'&sc='+ variety_ZZ[i] +'&cb=callback&callback=callback&_=1540896735401'
        f.write(variety_zz[i]+'\n')
        data_list = ProcessData(resp)
        AnalysisList(f,data_list)    
    f.close()
    print '--finish--'
  
        
def ProcessData(resp):    
    response = url.urlopen(resp)
    #response = requests.get(url)
    #response=url.urlopen(url)
    text = response.read()
    text_list = text.split('龙虎榜":[')
    
    data_list=[]
    #成交量 1 多持 2 空头持仓 6
    
    tmp = text_list[1].split('],"')
    data_list.append(tmp[0])
    
    tmp = text_list[2].split('],"')
    data_list.append(tmp[0])
    
    tmp = text_list[6].split('],"')
    data_list.append(tmp[0])        
    
    return data_list
    
def AnalysisList(f,data_list):
    
    data_vol  = {}
    data_buy  = {}
    data_sell = {}
    if len(data_list)>=3:
        tmp = data_list[0].split('"')
        
        for i in tmp:
            temp = i.split(',')
            if(len(temp) < 3):
                continue
            data_vol[temp[1]] = temp[2]
            
        tmp = data_list[1].split('"')
        
        for i in tmp:
            temp = i.split(',')
            if(len(temp) < 3):
                continue
            data_buy[temp[1]] = temp[2] 
            
        tmp = data_list[2].split('"')
        
        for i in tmp:
            temp = i.split(',')
            if(len(temp) < 3):
                continue
            data_sell[temp[1]] = temp[2]
            
        Analysis(f,data_vol,data_buy,data_sell)
         
def Analysis(f,data_vol,data_buy,data_sell):    
    #print data.columns
        
    dict = {}
    for(d,i) in data_vol.items():
        if(dict.has_key(d) == False):
            dict[d] = 0;
            
        dict[d] = dict[d]+1    
    
    for(d,i) in data_buy.items():
        if(dict.has_key(d) == False):
            dict[d] = 0;
            
        dict[d] = dict[d]+1
    
    
    for(d,i) in data_sell.items():
        if(dict.has_key(d) == False):
            dict[d] = 0;
            
        dict[d] = dict[d]+1
        
    dict_vol = {}
    num=0;
    tmp=0;
    for (d,x) in dict.items():
        if x>=3 :
            value_1 = float(data_vol[d]) 
            value_2 = float(data_buy[d])
            value_3 = float(data_sell[d])
            value = (value_2 + value_3)/value_1
            num+=1;
            tmp+=value;
            dict_vol[d]=value
    
    value_buy_1=0
    value_sell_1=0
    
    value_buy_0=0
    value_sell_0=0    
    for (d,x) in dict_vol.items():
        if x>=(tmp/num) :
            value_1 = float(data_vol[d]) 
            value_2 = float(data_buy[d])
            value_3 = float(data_sell[d])
            value = (value_2 - value_3)/(value_2 + value_3)
            op = ""
            if value > -0.12:
                value_buy_1 += value_2
                value_sell_1 += value_3
                op = ' buy '
            else:
                value_buy_0 += value_2
                value_sell_0 += value_3
                op = ' sell'
                
            f.write("\nname: "+ d + op + "  now: "+str(value) + u" 成交量: " + str(value_1) + u" 持买单量: " + str(value_2) + u" 持卖单量: " +   str(value_3))
    f.write("\nsell signal: " + u" 持买单量: " + str(value_buy_0) + u" 持卖单量: " + str(value_sell_0))
    f.write( "\nbuy  signal: " + u" 持买单量: " + str(value_buy_1) + u" 持卖单量: " + str(value_sell_1))
    f.write('\n\n\n')
    
# ITS = （持买单量-持卖单量）/（持买单量+持卖单量）        
        
   
    
def main():
    DownloadData()
    #ImportData()
    

if __name__=='__main__':
    main()