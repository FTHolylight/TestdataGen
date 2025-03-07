#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : ft

import pandas as pd
import numpy as np
import random
import string
from enum import Enum

# data_size=10
# data_contents=[
#     {
#         "field_name": "name",
#         "type": "str",
#         "range_begin": 1,
#         "range_end": 20,
#         "data_fixed_distribution": ["中国地区部","us","dn"],
#         "parent_data":"region",
#         "subdata_fixed_distribution": {"中国地区部": ["湖南代表处","广西代表处"], "us": []},
#         "subdata_fixed_distribution_flag": 0,
#         "unique_flag": 0
#     }
# ]


class GenType(Enum):
        GR_INT="TYPE_RANDOM_INT"
        GR_FLOAT="TYPE_RANDOM_FLOAT"
        GR_STR="TYPE_RANDOM_STR"
        GR_DATE="TYPE_RANDOM_DATE"
        GF_DATA="TYPE_FIEXD_DATA"
        GFS_DATA="TYPE_FIEXD_SUBDATA"

class DataGen:    
    @staticmethod
    def dataGen(data_size,data_contents: dict)->pd.DataFrame:
        datafam = pd.DataFrame()
        all_characters = string.ascii_letters + string.digits
        for data_item in data_contents:
            if "TYPE_RANDOM_INT"==data_item["type"]:
                #生成随机整数
                datafam[data_item["field_name"]] = np.random.randint(data_item["range_begin"], data_item["range_end"], size=data_size)

            elif "TYPE_RANDOM_FLOAT"==data_item["type"]:
                #生成随机浮点数
                datafam[data_item["field_name"]]  = np.random.uniform(data_item["range_begin"], data_item["range_end"], size=data_size)

            elif "TYPE_RANDOM_STRING"==data_item["type"]:
                # 生成二维字符数组并转换为一维字符串列表
                datafam[data_item["field_name"]] = [''.join(random.choices(all_characters, k=random.randint(data_item["range_begin"], data_item["range_end"]))) for _ in range(data_size)]
            
            elif "TYPE_RANDOM_DATE"==data_item["type"]:
                #生成随机日期
                datafam[data_item["field_name"]] = pd.date_range(data_item["range_begin"], periods=data_size, freq='D').tolist()

            elif "TYPE_FIEXD_DATA"==data_item["type"]:
                #生成指定数据
                datafam[data_item["field_name"]]=np.random.choice(data_item["data_fixed_distribution"],data_size)

            elif "TYPE_FIEXD_SUBDATA"==data_item["type"]:
                #生成依赖数据
                #TODO 判断子数据全生成标识是否为真 //为True这类处理要在其他指定了data_size生成后进行,因为会改变数据行数
                if data_item["subdata_fixed_distribution_flag"]==1:
                    subdata={data_item["parent_data"]:[],data_item["field_name"]:[]}
                    for key,valuse in data_item["subdata_fixed_distribution"].items():
                        subdata[data_item["parent_data"]].extend([key]*len(valuse))
                        subdata[data_item["field_name"]].extend(valuse)
                    datafam = pd.merge(datafam[data_item["parent_data"]], pd.DataFrame(subdata),on=data_item["parent_data"],how="left")
                else:
                    datafam[data_item["field_name"]]=datafam[data_item["parent_data"]].apply(lambda key:random.choice(data_item["subdata_fixed_distribution"][key]))
        return datafam
    
    




#测试数据
if __name__ == "__main__":
    df = pd.DataFrame({'category': ['A', 'B', 'C', 'A', 'B', 'C','A', 'B', 'C', 'A', 'B', 'C','A', 'B', 'C', 'A', 'B', 'C','A', 'B', 'C', 'A', 'B', 'C']
                    ,'id': [1, 2, 3, 4, 5, 6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]})
    a ={ 'A': ['Alpha','a','01',1],'B':['Beta','B','02',0] ,'C':['Gamma','c','03',1]}
    b={'category':[],'chi':[]}
    for key,value in a.items():
        b['category'].extend([key]*len(value))
        b['chi'].extend(value)    
    c =[{'a':1,'b':'b1','c':'c1'},{'a':0,'b':'b2','c':'c2'},{'a':1,'b':'b3','c':'c3'}]
    df=pd.merge(df,pd.DataFrame(b),on='category')
    print(sorted(c,key=lambda x:x['a'],reverse=True))



