import configparser
import os

def get_config(section, key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/config.conf'
    config.read(path,"utf-8")
    return config.get(section,key)

if __name__ == '__main__':
    data_info = get_config('database','dbhost')
    print(data_info)