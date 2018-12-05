# -*- coding: utf-8 -*-：
import itchat
import json
import requests
import codecs

sex_dict = {}
sex_dict['0'] = '其他'
sex_dict['1'] = '男'
sex_dict['2'] = '女'

def save_data(friend_list):
    out_file_name = "./data/friends.json"
    #fileObj = open(out_file_name,'w')
    with codecs.open(out_file_name, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(friend_list,ensure_ascii=False))
    '''
    for friend in friends_list:
        jsObj = json.dumps(friend)
        fileObj.write(jsObj)
        #fileObj.write('\n')
    
    fileObj.close()
    '''

def download_images(friends_list):
    image_dir = './images/'
    count = 1
    for friend in friends_list:
        image_name =str(count) +'.jpg'
        count +=1
        img = itchat.get_head_img(userName=friend["UserName"])
        with open(image_dir+image_name,'wb') as file:
            file.write(img)

def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    
    data = {
        'key' : 'b48a68f22aa93a821279274e301b093a',
        'info': msg,
        'userid':'wechat-robot'
        }
    
    
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return

@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    defaultReply = 'I received: ' + msg['Text']
    reply = get_response(msg['Text'])
    return reply or defaultReply
            
if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
    
    #itchat.send('Hello, filehelper',toUserName='filehelper')
    '''
    friends = itchat.get_friends(update=True)[0:]
    friends_list = []
    
    for friend in friends:
        item = {}
        item['NickName'] = friend['NickName']
        item['HeadImgUrl'] = friend['HeadImgUrl']
        item['Sex'] = sex_dict[str(friend['Sex'])]
        item['Province'] = friend['Province']
        item['Signature'] = friend['Signature']
        item['UserName'] = friend['UserName']
        friends_list.append(item)
        #print item
    save_data(friends_list)
    download_images(friends_list)
    print ('--finish--')
    '''
    