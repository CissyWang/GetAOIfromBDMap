# 获取baidu地图地点信息查询结果解析
# 表头为：'name','lng','lat','address','province','city','area','detail','uid'
import json
import pandas as pd
import requests
import time  # 控制时间暂停
import random  # 产生随机数
#已有列表爬取位置（小区/医院）

def address_json(test, xx):
    data = json.loads(test)
    final = pd.DataFrame(columns=('num', 'name', 'lng', 'lat', 'address', 'province', 'city', 'area', 'detail', 'uid'))
    for i in range(len(data['results'])):
        final.at[i, 'num'] = str(xx)
        final.at[i, 'name'] = data['results'][i]['name']
        final.at[i, 'lng'] = data['results'][i]['location']['lng']
        final.at[i, 'lat'] = data['results'][i]['location']['lat']
        try:
            final.at[i, 'address'] = data['results'][i]['address']
        except:
            final.at[i, 'address'] = 'x'
        final.at[i, 'province'] = data['results'][i]['province']
        final.at[i, 'city'] = data['results'][i]['city']
        final.at[i, 'area'] = data['results'][i]['area']

        # 新表新增的两列
        final.at[i, 'detail'] = data['results'][i]['detail']
        final.at[i, 'uid'] = data['results'][i]['uid']
        break
    return final


# 合成百度API地址
def address_web(name, city, lat, lng):
    # MyAK = 'w9HGFgmL64By3EbCf8ukfEIwx4uCqHjk'  # 自行申请的百度AK
    MyAK = 'HFly4BCwoY2f3kjcuopCR1nbFrF3YMho'  # 自行申请的百度AK

    query = 'query=' + name
    tag = 'tag=住宅'
    # keywords = 'query=' + name
    # types = 'types=120000'
    # key = 'key=fbb36c2d303c6de13b51d48b2f900d6e'

    # region = 'region=' + city
    loca = 'location=' + str(lat) + ',' + str(lng)
    rawstr = query + '&' + loca + '&' + tag + '&radius=2000&output=json&ak=' + MyAK
    # rawstr = query + '&' + tag + '&' + region + '&city_limit=true&output=json&ak=' + MyAK
    url = 'http://api.map.baidu.com/place/v2/search?' + rawstr
    # url = 'https://restapi.amap.com/v3/place/around?parameters' + rawstr
    return url

def address_web(name):
    # MyAK = 'w9HGFgmL64By3EbCf8ukfEIwx4uCqHjk'  # 自行申请的百度AK
    MyAK = 'HFly4BCwoY2f3kjcuopCR1nbFrF3YMho'  # 自行申请的百度AK

    query = 'query=' + name
    tag = 'tag=综合医院'
    region = 'region=' + '南京市'
    # loca = 'location=' + str(lat) + ',' + str(lng)
    # rawstr = query + '&' + loca + '&' + tag + '&radius=2000&output=json&ak=' + MyAK
    rawstr = query + '&' + tag + '&' + region + '&city_limit=true&output=json&ak=' + MyAK
    url = 'http://api.map.baidu.com/place/v2/search?' + rawstr

    return url


if __name__ == '__main__':
    respath = './result.csv'
    # 创建一个带有表头的空文件
    final = pd.DataFrame(columns=('num', 'name', 'lng', 'lat', 'address', 'province', 'city', 'area', 'detail', 'uid'))
    # final.to_csv(r'./result.csv', mode='a', header=True, index=False)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    # poi = pd.read_csv(
    #     r'./residential_new.csv')  # 读取小区名单
    poi = pd.read_csv(
        'E:\\BigData\\医疗\\二级以上综合医院列表.csv')  # 读取医院名单

    for i in range(9201, len(poi)):
        # 用于生成url
        # name = poi.loc[i, 'name']
        # city = poi.loc[i, 'city']
        name = poi.iloc[i, 1]
        city = '南京市'

        # lat = poi.loc[i, 'lat']
        # lng = poi.loc[i, 'lng']
        # url = address_web(name, city, lat, lng)  # 生成url
        url = address_web(name)

        wb_data = requests.get(url, headers=headers)  # 通过url和用户代理获取信息
        # wb_data = requests.get(url)  # 通过url和用户代理获取信息

        # 用于索引新表
        num = poi.iloc[i, 0]
        try:
            final = address_json(wb_data.text, num)
        except:
            print(num, '', name, ',', 'x')
            time.sleep(random.uniform(3.0, 15.0))  # 随机休眠
            continue

        # 输出
        if final.size > 0:
            print(str(num) + ',' + name + ',' + final.loc[0, 'uid'])
        final.to_csv(r'./result_a.csv', mode='a', header=False, index=False)
        # print(final)


        time.sleep(random.uniform(0.5, 2))  # 随机休眠
        # num += 1
    # 数据保存
    # final.to_csv(r'./result.csv', index=False)
