from mongo_db.mongodb_manager import DBManager
import matplotlib.pyplot as plt
import numpy as np

rate_fail = 0.7
period = 30
expect = 30

def draw_profit_bar(list1, list2):
    plt.subplot(111)
    lable_x = np.arange(len(list1))
    lable_y = [x*0 for x in range(len(list1))]
    
    plt.plot(lable_x, lable_y, color="404040", linewidth=1.0, linestyle="-")
    plt.bar(lable_x, list1, color="r", width=1.0)
    plt.bar(lable_x, list2, color='g', width=1.0)
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(list2) * 1.1, max(list1) * 1.1)
    plt.grid(True)
    plt.show()
    
if __name__ == '__main__':
    db_manager = DBManager("wm_details")
    code_list = db_manager.get_code_list()
    result_list = list()
    for item in code_list:
        code = item["code"][:6]
        print(code)
        tk_data = db_manager_wm.find_by_key({"code": code})[0]
        close_list = [float(x["close"]) for x in tk_data]