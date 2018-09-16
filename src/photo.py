# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import requests
import urllib
import re
import random
from time import sleep
from bs4 import BeautifulSoup


user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' 
cookies = 'd_c0="AGBCFLzclAyPTu9b86t_6uM3cR7C1fp8vSw=|1508928406"; _zap=fdff4608-bc81-4f26-a07c-91c6a45e75b4; __DAYU_PP=VQ6YfQUvaJJ6MJUbea6bffffffffec96e19475aa; z_c0="2|1:0|10:1532423377|4:z_c0|92:Mi4xd1o0ckFBQUFBQUFBWUVJVXZOeVVEQ1lBQUFCZ0FsVk4wVHBFWEFDOEFXZHR3UHhNakhXNEx5SVlTNl9iVHRKZHJB|2d146e39ba9cc3c996aa1854c298334ff5afb9a35daf4988574efbf4e53a6b8e"; q_c1=ad34f8d7cb954df39b1e9a50ca9396ef|1535549005000|1508928405000; __utma=51854390.1649593570.1536740076.1536740076.1536740076.1; __utmz=51854390.1536740076.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/20899988; __utmv=51854390.100-1|2=registration_date=20131229=1^3=entry_date=20131229=1; tgw_l7_route=c919f0a0115842464094a26115457122; _xsrf=31a4b96d-d77b-461a-8a91-3ba69c9e16b3'


def main():	
	url = 'https://www.zhihu.com/question/21844569/followers'
	
	#headers={'user-agent' : user_agent,'cookie':cookies}
	headers={'user-agent' : user_agent}
	i=1

	#for x in xrange(20,3600,20):
	
	for x in xrange(20,3600,20):

		data={"start":"0",
		"offset":str(x),
		"_xsrf":"IbzgcK4nmWdd2VBTX7vkwsVI8trRZUq4"}

		content=requests.post(url,headers=headers,data=data,timeout=10).text
		print content
		soup = BeautifulSoup(content,"html.parser")
		imgs = soup.find_all('img',class_='Avatar AuthorInfo-avatar')
		for img in imgs:
			try:
				print img['src']
				urllib.urlretrieve(img['src'],'E:/backup/'+str(i)+'.jpg')
				i=i+1
				sleep(random.uniform(0.5,1))
			except:
				print "miss one"
        		pass
        		sleep(random.uniform(0.5,1))
       	
        
        	
        
        
   

        
if __name__=='__main__':
	main()



