import requests
import pandas as pd
import json
import time
import numpy.random as random
#高德地图加了滑块反爬，只能用POI
# 检索POI的URL
poiUrl = "https://restapi.amap.com/v3/place/text?types=141201&city=南京&output=JSON&offset=20&key=fbb36c2d303c6de13b51d48b2f900d6e&extensions=all&page="
# 检索AOI的URL#网页加了滑块反爬……
aoiUrl = "https://ditu.amap.com/detail/get/detail?id="
# 用于储存POI数据
x = []
# 用于储存AOI数据
y = []
# 计数
num = 0
# 逐页POI检索，注意API限制
for page in range(1, 9):
    # 构造URL
    thisUrl1 = poiUrl + str(page)
    # 获取POI数据
    data1 = requests.get(thisUrl1)
    # 转为JSON格式
    s = data1.json()
    # 解析JSON
    aa = s["pois"]
    # 对每条POI进行读取
    for k in range(0, len(aa)):
        poiid = str(aa[k]["id"])
        # # 构造AOI的URL
        # thisUrl2 = aoiUrl + poiid
        # # 获取AOI数据
        # data2 = requests.get(thisUrl2)
        # # 转为JSON格式
        # ss = data2.json()
        # # 解析JSON
        # aaa = ss["data"]
        # key = aaa["spec"]
        #
        # # 判断AOI检索是否包含形状信息
        # haveShp = 0
        # for item in key:
        #     if item == "mining_shape":  # 有形状信息
        #         haveShp = 1
        # if haveShp == 0:
        #     continue  # 若无则跳出本条POI检索
        # 获取POI信息并存储
        pois1 = aa[k]["name"]
        pois2 = aa[k]["type"]
        pois3 = aa[k]["address"]
        pois4 = aa[k]["adname"]
        pois5 = aa[k]["location"].split(",")
        x.append([poiid, pois1, pois2, pois3, pois4, float(pois5[0]), float(pois5[1])])

        # 获取AOI信息并存储
        # aoilocs = str(key["mining_shape"]["shape"])
        # locs = aoilocs.split(';')
        # order = 0
        # for i in range(0, len(locs)):
        #     loc = locs[i].split(',')
        #     lon = loc[0]
        #     lat = loc[1]
        #     y.append([poiid, pois1, pois2, pois3, pois4, order, lon, lat])
        #     order += 1
        num += 1
        print("爬取了 " + str(num) + " POI数据")
        # time.sleep(random.randint(0, 5))  # 暂停0~3秒的整数秒，时间区间：[0,5]
# 将数据结构化存储至规定目录的CSV文件中
c1 = pd.DataFrame(x)
c1.to_csv('E:/greenland_Campus/poi.csv', encoding='utf-8-sig')
# c2 = pd.DataFrame(y)
# c2.to_csv('E:/aoi.csv', encoding='utf-8-sig')