#-*-coding:utf-8 -*-
import requests
import urllib2
import random
import json
from time import sleep
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def ru1901():
	tmp = 0
	while(1):
		url = 'http://hq.sinajs.cn/list=RU1901'
		response = urllib2.urlopen(url)
		result = response.read()
		
		result_split =  result.split(",")
		dict = {'Name:': 'Ru1901'}
	
		dict['open price:'] = result_split[2]
		dict['close priceL'] = result_split[5]
		dict['cur price:']   = result_split[6]
		dict['hightest price:'] = result_split[3]
		dict['lowest price:'] = result_split[4]

		if tmp != dict['cur price:']:
			print 'ru1901 cur price:'+dict['cur price:']
			tmp = dict['cur price:']
		sleep(random.uniform(0.1,0.2))

def ru1901history():
	url = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine5m?symbol=RU1901'
	#response = urllib2.urlopen(url)
	response = requests.get(url)
	r_json = response.json()
	r_lists = list(r_json)

	
	list_date=[]
	list_open=[]
	list_high=[]
	list_low=[]
	list_close=[]
	list_vol=[]
	for r_list in r_lists:
		if len(r_list) >= 5:
			list_date.append(r_list[0])
			list_open.append(r_list[1])
			list_high.append(r_list[2])
			list_low.append(r_list[3])
			list_close.append(r_list[4])

	df = pd.DataFrame({'date':list_date,'open':list_open,'high':list_high,'low':list_low,'close':list_close})
	columns=['date','open','high','low','close']
	df.to_csv('ru1901.csv',index=False,columns=columns)

def ewma(s,n):
	f = 2.0/(n+1)
	
	data = []
	for i in range(0,len(s)-1):
		if i == 0:
			data.append(s[i])
		else:
			result = (f* (s[i]) + (1-f)*(s[i-1]))
			data.append(result)

	return data



# 26 12 9
def macd():
	data = pd.read_csv('ru1901.csv',parse_dates=[1])
	data.sort_values('date',inplace=True)
	value_len = len(data['close'])
	DI = []
	for i in range(len(data['close'])):
		value  = (data['close'][i] *2 + data['high'][i] + data['low'][i])/4.0 
		DI.append(value)

	ema_12 = ewma(DI, 12)
	ema_26 = ewma(DI, 26)
	DIF = []
	MACD_BAR = []

	for i in range(0,len(ema_12)):
		DIF.append(ema_12[i] - ema_26[i])
		
	macd_9 = ewma(DIF,9)

	for i in range(0,len(macd_9)):
			MACD_BAR.append(DIF[i] - macd_9[i])
	plt.plot(macd_9)
	plt.plot(DIF)
	plt.bar(range(len(macd_9)), MACD_BAR)
	plt.show()



def openCloseStrategy():
	data = pd.read_csv('ru1901.csv',parse_dates=[1])

	data.sort_values('date',inplace=True)
	
	#print data['open']
	#data['MA_' + str(5)] = pd.rolling_mean(data['open'],10)
	
	close_data = np.array(ewma(data['close'], 5))
	open_data  = np.array(ewma(data['open'], 5))
	
	open_data = open_data.astype('float64')
	#print open_data.dtype
	#print close_data.dtype
	train_data = []
	#print len(open_data)
	#print len(close_data)
	min_range =  min(len(open_data),len(close_data))
	
	for i in range(0, min_range):
		train_data.append(close_data[i] - open_data[i])

	plt.bar(range(min_range), train_data)
	#plt.plot(train_data)
	plt.show()
	
	'''
	train_data = np.array(data)
	train_data_list = train_data.tolist()
	train_data_list.reverse()
	
	list_date=[]
	list_open=[]
	list_high=[]
	list_low=[]
	list_close=[]
	list_vol=[]
	for r_list in train_data_list:
		if len(r_list) >= 5:
			list_date.append(r_list[0])
			list_open.append(r_list[1])
			list_high.append(r_list[2])
			list_low.append(r_list[3])
			list_close.append(r_list[4])

	data_ema = pd.ema(list_open,span=10)[-1]
	'''
	


def main():
	#ru1901()
	#ru1901history()
	#openCloseStrategy()
	macd()

    

if __name__ == '__main__':
	main()