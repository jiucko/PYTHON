# -*- coding: utf-8 -*-
import sys
import os

o_path = os.getcwd()
father_path=os.path.abspath(os.path.dirname(o_path)+os.path.sep+".")
sys.path.append(father_path) 

import datetime

import redis

from config import mod_config
from mongo_db.mongodb_manager import DBManager

def cmp_datatime(item):
    return datetime.datetime.strptime(item["cur_timer"],"%Y-%m-%d")

class RedisManager:
    def __init__(self):
        self.pool = redis.ConnectionPool(host=mod_config.get_config("redis", "redis_host"), port=mod_config.get_config("redis", "redis_port"), decode_responses=True)
        self.r = redis.Redis(connection_pool=self.pool)
        
    def update_data(self):
        print("-redis_start-")
        dm = DBManager("wm_details")
        code_list = dm.get_code_list()
        for item in code_list:
            try:
                code = item["code"][:6]
                _result = dm.find_by_id(item["code"])
                sorted_result = sorted(_result["price_list"],key = lambda x:cmp_datatime(x), reverse=True)
                self.set_data(code,sorted_result)
            except Exception:
                print("redis_error:501 "+str(item["code"]))       
        print("-redis_close-")
        
    def get_data(self, key=""):
        if key:
            _result = self.r.get(key)
            if _result:
                return _result
        return []
    
    def set_data(self, key, value):
        if key:
            self.r.set(key, value)
            
if __name__ == '__main__':
    rm = RedisManager()
    rm.update_data()
            