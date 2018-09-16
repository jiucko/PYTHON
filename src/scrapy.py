
# -*- coding: UTF-8 -*-

import urllib2
import cookielib
import re

from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

'''
response = urllib.urlopen('https://www.baidu.com/')
result = response.read()
print(result)


url = "https://design-patterns.readthedocs.io/zh_CN/latest/read_uml.html"
response1 = urllib2.urlopen(url)

result = response1.read()
print(result)


print response1.getcode()
print len(response1.read())


#way two

request = urllib2.Request(url)
request.add_header("user-agent","Mozilla/5.0")
response2 = urllib2.urlopen(request)
print response2.getcode()
print len(response2.read())
'''
#way three

cookie = urllib2.Request(url)
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)
response3 = urllib2.urlopen(url)
print response3.getcode()
print len(response3.read())
print cookie


'''
html_doc = """ 
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
soup = BeautifulSoup(result,"html.parser",from_encoding="utf_8")

links = soup.find_all('a')
print "all the links"

for link in links :
	print link.name,link['href'],link.get_text()

print "get sprcial link"
link_node = soup.find('a',href="http://example.com/elsie")
print link_node.name,link_node['href'],link_node['class'],link_node.get_text()

print "re"
link_node = soup.find('a',href=re.compile(r"ti"))
print link_node.name,link_node['href'],link_node['class'],link_node.get_text()

print "context"
p_node = soup.find('p',class_='story')
print p_node.name, p_node['class'],p_node.get_text()
'''