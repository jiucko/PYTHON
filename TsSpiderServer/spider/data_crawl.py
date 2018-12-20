from time import sleep
import gc
import bs4
from datetime import datetime

import requests
import sys
sys.path.append('F:\\PYTHON\\TsSpiderServer\\')
from mongo_db.mongodb_manager import DBManager

def get_cur_season():
    _year = datetime.now().date().year
    _month = datetime.now().date().month
    if int(_month) <=3:
        _season = 1
    elif int(_month)<=6:
        _season = 2
    elif int(_month)<= 9:
        _season = 3
    else:
        _season = 4
        
    return str(_year),str(_season)

class DataCrawl:
    def __init__(self):
        self.dm = DBManager("wm_details")
        self.headers = {
            "User-Agent":":Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }
    
    def start_crawl(self):
        print("-start up-")
        _year,_season = get_cur_season()
        self.get_url(_year,_season)
    
    def end_crawl(self):
        self.dm.close_db()
        
    def get_url(self, year, season):
        code_list = self.dm.get_code_list()
        for item in code_list:
            key = item["code"][:6]
            url = "http://quotes.money.163.com/trade/lsjysj_" + key + ".html?year=" + year + "&season=" + season
            print(url)
            
            max_try = 8
            for tries in range(max_try):
                try:
                    content = requests.get(url)
                    self.parse_pager(content.content, item["code"])
                    break
                except Exception:
                    if tries < (max_try -1):
                        sleep(2)
                        continue
                    else:
                        print("ERROR TO DOWNLODE DATE")
        code_list.close()
    
    def parse_pager(self,content, key):
        try:
            _result = self.dm.find_by_id(key)
            timer_list = [x["cur_timer"] for x in _result["price_list"]]
            soup = bs4.BeautifulSoup(content,"lxml")
            parse_list = soup.select("div.inner_box tr")
            for item in parse_list[1:]:
                data = [x.string for x in item.select("td")]
                price = {
                    "cur_timer": data[0],
                    "cur_open_price": data[1],
                    "cur_max_price": data[2],
                    "cur_min_price": data[3],
                    "cur_close_price": data[4],
                    "cur_price_range": data[6],
                    "cur_total_volume": data[7],
                    "cur_total_money": data[8]
                }
                if price["cur_timer"] not in timer_list:
                    self.dm.add_tk_item(key,price)
            print(key,"success")
        except Exception:
            print(key,"faild")
            
if __name__ == '__main__':
    dc = DataCrawl()
    dc.start_crawl()
    print("--finish--")
            