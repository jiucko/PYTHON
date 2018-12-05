#coding=utf-8

import json
import re

from pyecharts import Bar
from pyecharts import Grid
from pyecharts import WordCloud
from pyecharts import Pie
from pyecharts import Map
from collections import Counter

import jieba.analyse 
import PIL.Image as Image
import os
import math

def dict2list(_dict):
    name_list = []
    num_list = []
    
    for key,value in _dict.items():
        name_list.append(key)
        num_list.append(value)
    
    return name_list,num_list

def counter2list(_counter):
    name_list = []
    num_list = []
    
    for item in _counter:
        name_list.append(item[0])
        num_list.append(item[1])
    
    return name_list,num_list


def get_tag(text,cnt):
    text = re.sub(r"<span.*><span>", "", text)
    print('正在分析句子:',text)
    if(text == ""):
        return;
    tag_list = jieba.analyse.extract_tags(text)
    for tag in tag_list:
        if(tag == 'span' or tag.find('emoji')!=-1 or tag=='class'):
            continue
        cnt[tag] += 1

def get_pie(item_name, item_name_list,item_num_list):
    total = item_num_list[0]+item_num_list[1]+item_num_list[2]
    subtitle = "共有:"+str(total)+"个好友"
    pie = Pie(item_name,page_title = item_name,title_text_size=30,title_pos='center',\
        subtitle = subtitle,subtitle_text_size = 25,width=800,height= 800)
    
    pie.add("", item_name_list, item_num_list,is_label_show=True,center=[50, 45],radius=[0,50],\
        legend_pos ='left',legend_orient='vertical',label_text_size=20)

    out_file_name = './analyse/'+item_name+'.html'
    #print(out_file_name)
    pie.render(out_file_name)
 
def get_bar(item_name,item_name_list,item_num_list):
    subtitle = ""
    bar = Bar(item_name,page_title=item_name,title_text_size=30,title_pos='center',\
                subtitle = subtitle,subtitle_text_size = 25)
    bar.add("",item_name_list,item_num_list,title_pos='center',xaxis_interval=0,xaxis_rotate=27,\
             xaxis_label_textsize = 20,yaxis_label_textsize = 20,yaxis_name_pos='end',yaxis_pos = "%50")
     
    grid = Grid(width=1300,height= 800)
    grid.add(bar,grid_top = "13%",grid_bottom = "23%",grid_left = "15%",grid_right = "15%")
    out_file_name = './analyse/'+item_name+'.html'
    grid.render(out_file_name)
 
def get_map(item_name,item_name_list,item_num_list):
    subtitle = ""
    _map = Map(item_name,width=1300,height=800,title_pos='center',title_text_size=30,\
               subtitle = subtitle,subtitle_text_size = 25)
    _map.add("",item_name_list,item_num_list,maptype='china',is_visualmap=True,visual_text_color='#000')
    
    out_file_name = './analyse/'+item_name+'.html'
    _map.render(out_file_name)

def word_cloud(item_name,item_name_list,item_num_list,word_size_range):

    wordcloud = WordCloud(width=1400,height= 900)
    
    wordcloud.add("", item_name_list, item_num_list,word_size_range=word_size_range,shape='pentagon')
    out_file_name = './analyse/'+item_name+'.html'
    wordcloud.render(out_file_name)

def mergeImage():
    print("正在合成头像")
    photo_width = 200
    photo_height = 200
    
    photo_path_list = []
    
    dirName = os.getcwd()+'/images'
    for root, dirs, files in os.walk(dirName):
        for file in files:
            if "jpg" in file and os.path.getsize(os.path.join(root, file)) > 0:
                photo_path_list.append(os.path.join(root, file))

    pic_num = len(photo_path_list)
    line_max = int(math.sqrt(pic_num))
    row_max = int(math.sqrt(pic_num)) 
    
    num = 0
    pic_max=line_max*row_max
    toImage = Image.new('RGBA',(photo_width*line_max,photo_height*row_max))
    
    for i in range(0,row_max):
        for j in range(0,line_max):
            pic_fole_head =  Image.open(photo_path_list[num])
            width,height =  pic_fole_head.size
        
            tmppic = pic_fole_head.resize((photo_width,photo_height))
        
            loc = (int(j%row_max*photo_width),int(i%row_max*photo_height))
            toImage.paste(tmppic,loc)
            num= num+1
        
            if num >= len(photo_path_list):
                break
        
            if num >= pic_max:
                break   
            
        print(toImage.size)
        toImage.save('./analyse/merged.png')
            
    
    
if __name__ == '__main__':
    file_name = './data/friends.json'
    friends = {}
    with open(file_name,'r',encoding='UTF-8') as load_f:
        friends = json.load(load_f)
    print (friends)
    
    #待统计参数
    sex_counter = Counter()
    Province_counter = Counter()
    NickName_list = []
    Signature_Counter = Counter()
    
    for friend in friends:
        sex_counter[friend['Sex']] += 1
        if friend['Province'] != '':
            Province_counter[friend['Province']] += 1
        NickName_list.append(friend['NickName'])
        get_tag(friend['Signature'],Signature_Counter)
    
    name_list,num_list = dict2list(sex_counter)
    get_pie('性别统计',name_list,num_list)
    
    name_list,num_list = dict2list(Province_counter)
    get_bar('地区统计',name_list,num_list)
    
    get_map('地区地图统计',name_list,num_list)
    
    num_list = [5 for i in range(1,len(NickName_list)+1)]
    word_cloud('微信好友昵称',NickName_list,num_list,[18,18])
    
    name_list,num_list = counter2list(Signature_Counter.most_common(200))
    word_cloud('微信好友签名关键词',name_list,num_list,[20,100])
    
    mergeImage()
    print("--finish--")