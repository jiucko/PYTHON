# -*- coding: utf-8 -*-：
import requests
import json



apiUrl = 'http://www.tuling123.com/openapi/api'

data = {
    'key' : 'b48a68f22aa93a821279274e301b093a',
    'info': 'hello',
    'userid':'wechat-robot'
    }

r = requests.post(apiUrl, data=data).json()
'''
rep = requests.post(apiUrl, data)
rep.encoding = 'utf-8'


reps = rep.json().get('text')
re_url = rep.json().get('url')
re_lists = rep.json().get('lists')
'''
reps = r.get('text')  

    
print(reps)