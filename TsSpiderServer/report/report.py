import sys
import os

o_path = os.getcwd()
father_path=os.path.abspath(os.path.dirname(o_path)+os.path.sep+".")
sys.path.append(father_path)
from mongo_db.mongodb_manager import DBManager
import matplotlib.pyplot as plt
import numpy as np

rate_fail = 0.7
period = 30
expect = 30

def draw_profit_bar(list1, list2):
    plt.subplot(111)
    lable_x = np.arange(len(list1))
    lable_y = [x * 0 for x in range(len(list1))]
    
    plt.plot(lable_x, lable_y, color="#404040", linewidth=1.0, linestyle="-")
    plt.bar(lable_x, list1, color="r", width=1.0)
    plt.bar(lable_x, list2, color="g", width=1.0)
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(list2) * 1.1, max(list1) * 1.1)
    plt.grid(True)
    plt.show()
    
if __name__ == '__main__':
    db_manager = DBManager("wm_details")
    code_list = db_manager.get_code_list()
    result_list = list()
    for item in code_list:
        code = item["code"]
        print(code)
        tk_data = db_manager.find_by_key({"code": code})[0]
        close_list = [float(x["cur_close_price"]) for x in tk_data["price_list"] if x["cur_close_price"] != 0]
        len_list = len(close_list)
        if close_list:
            for index in range(expect, len(close_list)):
                rate_1 = (close_list[index-period] - close_list[index]) / close_list[index - period]
                if rate_1 > rate_fail and len_list > index+expect:
                    exp_top = max(close_list[index+1: index+expect])
                    exp_low = min(close_list[index+1: index+expect])
                    rate_2 = (exp_top - close_list[index]) / close_list[index]
                    rate_3 = (exp_low - close_list[index]) / close_list[index]
                    result_list.append({"rate_1": rate_1, "rate_2": rate_2, "rate_3": rate_3})
                    
    draw_profit_bar([x["rate_2"] for x in result_list], [x["rate_3"] for x in result_list])    