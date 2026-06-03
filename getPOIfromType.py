
# 表头为：'name','lng','lat','address','province','city','area','detail','uid'
import json
import pandas as pd
import requests
import time  # 控制时间暂停
import random  # 产生随机数
# 尝试百度地图爬取整个城市的医疗服务设施，有页数限制

# 合成百度API地址
def address_web(num):
    MyAK = '****************'  # 自行申请的百度AK

    query = 'query=' + '医疗'
    region = 'region=' + '南京市'
    tag = 'tag='+'医疗'
    # 诊所、药店、体检机构、疗养院、急救中心、疾控中心、医疗器械、医疗保健、其他
    rawstr = query + '&' + tag + '&' + region + '&city_limit=true&output=json&page_size=20&ak=' + MyAK
    url = 'http://api.map.baidu.com/place/v2/search?' + rawstr + '&page_num=' + str(num)

    return url


if __name__ == '__main__':
    respath = './result.csv'
    # 创建一个带有表头的空文件
    final = pd.DataFrame(columns=('num', 'name', 'lng', 'lat', 'address', 'province', 'city', 'area', 'detail', 'uid'))
    # final.to_csv(r'./result.csv', mode='a', header=True, index=False)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}


    index = 0

    for i in range(100):
        url = address_web(i)
        wb_data = requests.get(url, headers=headers)
        data = json.loads(wb_data.text)
        data_result = data['results']
        # print(data)
        try:
            print(len(data_result))
        except:
            print('404')
        # for j in range(len(data_result)):
        #     final.at[index, 'name'] = j['name']
        #     final.at[index, 'lng'] = j['location']['lng']
        #     final.at[index, 'lat'] = j['location']['lat']
        #     final.at[index, 'address'] = j['location']['address']
        #     final.at[i, 'area'] = data['results'][0]['area']

        time.sleep(random.uniform(0.5, 2))  # 随机休眠



    # try:
    #
    #     final.at[i, 'name'] = data['results'][0]['name']
    #     final.at[i, 'lng'] = data['results'][0]['location']['lng']
    #     final.at[i, 'lat'] = data['results'][0]['location']['lat']
    #     final.at[i, 'address'] = data['results'][0]['address']
    #     # try:
    #     #     final.at[i, 'address'] = data['results']['address']
    #     # except:
    #     #     final.at[i, 'address'] = 'x'
    #     final.at[i, 'rank1'] = poi.iloc[i, 4]
    #     final.at[i, 'rank2'] = poi.iloc[i, 5]
    #     final.at[i, 'area'] = data['results'][0]['area']
    #
    #     # 新表新增的两列
    #     final.at[i, 'type'] = poi.iloc[i, 6]
    #     final.at[i, 'uid'] = data['results'][0]['uid']
    # except:
    #     print(i, '', name, ',', 'x')
    # for i in range(9201, len(poi)):
        # 用于生成url
        # url = address_web()
        # wb_data = requests.get(url, headers=headers)  # 通过url和用户代理获取信息
        # wb_data = requests.get(url)  # 通过url和用户代理获取信息

        # 用于索引新表
        # try:
        #     final = address_json(wb_data.text, i)
        # except:
        #     print(i, '', name, ',', 'x')

        # 输出
        # if final.size > 0:
        #     print(str(i) + ',' + name + ',' + final.loc[0, 'uid'])
        # final.to_csv(r'./result_yiliao.csv', mode='a', header=False, index=False)
        # # print(final)
        #
        #
        # time.sleep(random.uniform(0.5, 2))  # 随机休眠
        # num += 1
    # 数据保存
    # final.to_csv(r'./result.csv', index=False)
