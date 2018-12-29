# -*- coding: utf-8 -*-
from datetime import datetime

from pymongo import MongoClient

from config import mod_config

class DBManager:
    def __init__(self, table_name):
        """
        连接MongoClient
        由3种方法可以选择，看使用情况
        """
        self.client = MongoClient(mod_config.get_config("database","dbhost"),int(mod_config.get_config("database","dbport")))
        self.db = self.client[mod_config.get_config("database","dbname")]
        self.table = self.db[table_name]
        
    def close_db(self):
        self.client.close()
        
    def add_one(self, post, created_time=datetime.now()):
        """
        添加一条数据
        需要注意的是Mongo中不需要事先建立表，插入数据的同时直接根据所传入字典对象的内容生成表
        """
        post['created_time'] = created_time
        return self.table.insert_one(post)
    
    def push_one(self, where, push):
        return self.table.update_one(where, {"$push":push})
    
    def add_futures_item(self, code, data_item):
        return self.table.update_one({'code': code}, {"$push": {"details": data_item}})
    
    def add_tk_item(self, tk_code, price_item):
        return self.table.update_one({'code':tk_code},{"$push":{"price_list":price_item}})
    
    def find_by_id(self, tk_code="",request={}):
        """
        通过tk_code查找数据
        """
        if tk_code:
            request["code"] = tk_code
            return self.table.find_one(request)
        else:
            return self.table.find({}, no_cursor_timeoyt=True)
    
    def get_code_list(self):
        return self.table.find({},{"code":1},no_cursor_timeout=True)
        
    def find_one_by_key(self, request={}):
        return self.table.find_one(request)   
    
    def find_by_key(self, request=[]):
        return self.table.find(request)