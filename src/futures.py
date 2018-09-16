#-*-coding:utf-8 -*-
import requests
import urllib2
import random
import json
from time import sleep
import pandas as pd
import numpy as np

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
	f = 2/(n+1)

	data = []
	for i in range(len(s)):
		if i == 0:
			data.append(s[i])
		result = f*s[i] + (1-f)*s[i-1]
		data.append(result)

	return data



def openCloseStrategy():
	data = pd.read_csv('ru1901.csv',parse_dates=[1])

	data.sort_values('date',inplace=True)
	
	#print data['open']
	#data['MA_' + str(5)] = pd.rolling_mean(data['open'],10)
	data['EMA_' + str(5)] = ewma(data['close'], 10)


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
	openCloseStrategy()

    

if __name__ == '__main__':
	main()