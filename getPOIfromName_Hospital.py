# 获取高德地图地点信息查询结果解析
# 表头为：'name','lng','lat','address','province','city','area','detail','uid'
import json
import pandas as pd
import requests
import time  # 控制时间暂停
import random  # 产生随机数


def address_json(test, xx):
    data = json.loads(test)
    final = pd.DataFrame(columns=('name', 'lng', 'lat', 'address', 'rank1', 'rank2', 'area', 'type', 'own' 'uid'))
    for i in range(len(data['results'])):

        final.at[i, 'name'] = data['results'][i]['name']
        final.at[i, 'lng'] = data['results'][i]['location']['lng']
        final.at[i, 'lat'] = data['results'][i]['location']['lat']
        try:
            final.at[i, 'address'] = data['results'][i]['address']
        except:
            final.at[i, 'address'] = 'x'
        final.at[i, 'province'] = data['results'][i]['province']
        final.at[i, 'rank1'] = data['results'][i]['city']
        final.at[i, 'area'] = data['results'][i]['area']

        # 新表新增的两列
        final.at[i, 'detail'] = data['results'][i]['detail']
        final.at[i, 'uid'] = data['results'][i]['uid']
        break
    return final


# 合成百度API地址
def address_web(name):
    MyAK = '*******************'  # 自行申请的百度AK

    query = 'query=' + name
    tag = 'tag=综合医院'
    region = 'region=' + '南京市'
    rawstr = query + '&' + tag + '&' + region + '&city_limit=true&page_size=1&output=json&ak=' + MyAK
    url = 'http://api.map.baidu.com/place/v2/search?' + rawstr

    return url


if __name__ == '__main__':
    # respath = './result.csv'
    # 创建一个带有表头的空文件
    final = pd.DataFrame(columns=('name', 'lng', 'lat', 'address', 'rank1', 'rank2', 'area', 'type', 'uid'))
    final.to_csv(r'./result.csv', mode='a', header=True)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

    poi = pd.read_csv(
        'E:\\BigData\\医疗\\二级以上综合医院列表.csv')  # 读取医院名单

    for i in range(len(poi)):
        # 用于生成url
        name = poi.iloc[i, 1]

        city = '南京市'
        url = address_web(name)
        wb_data = requests.get(url, headers=headers)  # 通过url和用户代理获取信息
        data = json.loads(wb_data.text)
        # print(data['results'][0])
        try:

            # final = pd.DataFrame(
            #     columns=('name', 'lng', 'lat', 'address', 'rank1', 'rank2', 'area', 'type', 'uid'))
            final.at[i, 'name'] = data['results'][0]['name']
            final.at[i, 'lng'] = data['results'][0]['location']['lng']
            final.at[i, 'lat'] = data['results'][0]['location']['lat']
            final.at[i, 'address'] = data['results'][0]['address']
            # try:
            #     final.at[i, 'address'] = data['results']['address']
            # except:
            #     final.at[i, 'address'] = 'x'
            final.at[i, 'rank1'] = poi.iloc[i,4]
            final.at[i, 'rank2'] = poi.iloc[i,5]
            final.at[i, 'area'] = data['results'][0]['area']

            # 新表新增的两列
            final.at[i, 'type'] = poi.iloc[i,6]
            final.at[i, 'uid'] = data['results'][0]['uid']
        except:
            print(i, '', name, ',', 'x')


        # 输出
        if final.size > 0:
            print(i, ',' + name, ',' + final.loc[0, 'uid'])
        time.sleep(random.uniform(0.5, 2))  # 随机休眠
        final.to_csv('E:\\BigData\\医疗\\hospital.csv', index=True, mode='a', header=False)
    print(final)




