import sys
import os

o_path = os.getcwd()
father_path=os.path.abspath(os.path.dirname(o_path)+os.path.sep+".")
sys.path.append(father_path) 

from urllib import request
from datetime import datetime
import time
import pandas as pd
import json

from pandas.tseries.offsets import BDay

from config import mod_config


instList = [{
    "xchg": "SHFE",
    "inst": [ "ru"]
}, {
    "xchg": "SHFE2",
    "inst": []
}, {
    "xchg": "SHFE3",
    "inst": ["hc", "ni", "rb", "zn"]
}, {
    "xchg": "CZCE",
    "inst": [ "ma", "sr", "zc"]
}, {
    "xchg": "DCE",
    "inst": ["j","jm","jd","m",]
}]

def hxAnalysis():
    cur_time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    for i in instList:
        for j in i['inst']:
            code = i['xchg']+mod_config.get_config(j,"variety")
            url = 'http://webftcn.hermes.hexun.com/shf/kline?code=' + code + '&start=' + cur_time + '&number=-720&type=1'
            print('----' + str(j) + ' begin -------')
            hxRecords(url,j)
            print('----' + str(j) + ' end   -------')

def hxRecords(url,variety):
    resp = request.urlopen(url)
    resp = resp.read()[1:-2]
    resp=json.loads(resp)['Data']
    re=[]
    pw=float(resp[4])
    for i in resp[0]:
        res=dict(Time=time.mktime(time.strptime(str(i[0]),'%Y%m%d%H%M%S'))*1000,Open=i[2]/pw,High=i[4]/pw
                ,Low=i[5]/pw,Close=i[3]/pw,Volume=i[6])
        
        re.append(res)
        
    find_top_shape(cal_macd(re,variety),variety)

def cmp_date(variety,date):
    start_time = mod_config.get_config(variety,"start_time")
    s_time = time.mktime(time.strptime(start_time,'%Y%m%d%H%M%S'))*1000
    return date >= s_time

def cmp_date_grater(variety,date):
    start_time = mod_config.get_config(variety,"start_time")
    s_time = time.mktime(time.strptime(start_time,'%Y%m%d%H%M%S'))*1000
    return date > s_time

def cal_macd(data, variety):
    start_time = mod_config.get_config(variety,"start_time")
    work_day = int(mod_config.get_config("global","work_day"))
    date = (pd.datetime.today() - BDay(work_day)).strftime('%Y%m%d')   
    s_time = time.mktime(time.strptime(date,'%Y%m%d'))*1000
    need_reset = False
    if cmp_date_grater(variety,s_time):
        new_start = s_time + 21*60*60*1000
        need_reset = True
    ema_12,ema_26,dea = cal_ema(variety)
    diff = ema_12 - ema_26
    for i in data:
        if cmp_date(variety,i['Time']) == False:
            continue       
        if cmp_date_grater(variety,i['Time']):
            ema_12 = ema_12 * (11 / 13.0) + i['Close'] * (2 / 13.0)
            ema_26 = ema_26 * (25 / 27.0) + i['Close'] * (2 / 27.0)
            diff = ema_12 - ema_26
            dea = dea * (8/10.0) + diff * (2/10.0)
            if need_reset and i['Time'] == new_start:
                need_reset = False
                mod_config.set_config(variety,"ema_12",str(ema_12))
                mod_config.set_config(variety,"ema_26",str(ema_26))
                mod_config.set_config(variety,"dea",str(dea))
                mod_config.set_config(variety,"start_time",time.strftime('%Y%m%d%H%M%S',time.localtime(new_start/1000)))
                               
        i.update(Dif = diff)
        i.update(Dea = dea)

    return data
        
def cal_ema(variety):
    ema_12 = mod_config.get_config(variety,"ema_12")
    ema_26 = mod_config.get_config(variety,"ema_26")
    dea = float(mod_config.get_config(variety,"dea"))
    if ema_12=="" :
        diff_1 = float(mod_config.get_config(variety,"diff_1"))
        diff_2 = float(mod_config.get_config(variety,"diff_2"))
        next_price = float(mod_config.get_config(variety,"next_price"))
        ema_26 = (28 * next_price - (351 * diff_2 - 297 * diff_1))/28.0
        ema_12 = diff_1 + ema_26
        mod_config.set_config(variety,"ema_12",str(ema_12))
        mod_config.set_config(variety,"ema_26",str(ema_26))
    return float(ema_12),float(ema_26),dea

def find_top_shape(data,variety):
    first_k = data[0];
    sec_k = data[1] 
    flag = 0;
    if(first_k['Low']) < sec_k['Low']:
        flag = 1
    count = 0
    real_count = 0
    is_top = True;
    last_k = first_k
    top_list = []

    for i in range(2,len(data)):
        if (sec_k['High'] >= data[i]['High'] and sec_k['Low'] <= data[i]['Low']) or (sec_k['High'] <= data[i]['High'] and sec_k['Low'] >= data[i]['Low']):
            sec_k['Time'] = data[i]['Time']
            if flag == 1:
                sec_k['Low'] = max(data[i]['Low'],sec_k['Low'])
                sec_k['High'] = max(data[i]['High'],sec_k['High'])
            else:
                sec_k['Low'] = min(data[i]['Low'],sec_k['Low'])
                sec_k['High'] = min(data[i]['High'],sec_k['High'])
            real_count +=1
            continue;
        if first_k['Low'] < sec_k['Low'] and data[i]['Low'] < sec_k['Low'] and first_k['High'] < sec_k['High'] and data[i]['High'] < sec_k['High']:
            if (len(top_list) >0 and top_list[-1]['is_top'] == False and count > 5 and sec_k['High'] > top_list[-1]['High']) or len(top_list) == 0:
                sec_k['is_top'] = True
                top_list.append(sec_k)
                count = 0
            elif sec_k['High'] > top_list[-1]['High'] and top_list[-1]['is_top'] == True:
                sec_k['is_top'] = True
                top_list[-1] = sec_k
                count = 0
         
        if first_k['Low'] > sec_k['Low'] and data[i]['Low'] > sec_k['Low'] and first_k['High'] > sec_k['High'] and data[i]['High'] > sec_k['High']:
            if (len(top_list) >0 and top_list[-1]['is_top'] == True and count > 5 and sec_k['Low'] < top_list[-1]['Low']) or len(top_list) == 0:
                sec_k['is_top'] = False
                top_list.append(sec_k)
                count = 0
            elif sec_k['Low'] < top_list[-1]['Low'] and top_list[-1]['is_top'] == False:
                sec_k['is_top'] = False
                top_list[-1] = sec_k
                count = 0
    
        first_k = sec_k
        sec_k = data[i]
        count += 1
        if(first_k['Low']) < sec_k['Low']:
            flag = 1
        else:
            flag = 0
            
    for i in range(len(top_list)):
        if i > 2 and cmp_date(variety,top_list[i - 2]['Time']):
            if top_list[i]['is_top'] and top_list[i]['High'] > top_list[i-2]['High'] and max(top_list[i]['Dif'], top_list[i]['Dea']) < max(top_list[i-2]['Dif'], top_list[i-2]['Dea']):
                print('--top--')
                print(time.localtime(top_list[i]['Time']/1000))
                print(top_list[i])
            elif top_list[i]['is_top']==False and top_list[i]['Low'] < top_list[i-2]['Low'] and min(top_list[i]['Dif'], top_list[i]['Dea']) > min(top_list[i-2]['Dif'], top_list[i-2]['Dea']):
                print('--bottom--')
                print(time.localtime(top_list[i]['Time']/1000))
                print(top_list[i]) 
    

if __name__ == '__main__':
    hxAnalysis()
    print('-finish-')