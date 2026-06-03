# 爬取AOI 简化后
import csv

# import pandas as pd
# import requests
# import time #控制时间暂停
# import random #产生随机数
# import json
# 将列表坐标处理位','和';'间隔的字符串
# 返回米制坐标转经纬度链接
# http://api.map.baidu.com/geoconv/v1/?coords=114.21892734521,29.575429778924&from=6&to=5&ak=sfW*************ACnzp //GET请求

# 自定义函数：AK改为自己的,多个坐标用‘；’间隔
# 合成坐标转换申请链接：百度米制坐标转百度经纬度

def bdzb_url(geo):
    num = int((len(geo) - 1) / 2)
    geox = ''
    for n in range(num):
        tx = str(geo[2 * n]) + ',' + str(geo[2 * n + 1])
        geox = geox + ';' + tx
    bdzb_url = 'http://api.map.baidu.com/geoconv/v1/?coords=' + geox.lstrip(
        ';') + '&from=6&to=5&ak=w9HGFgmL64By3EbCf8ukfEIwx4uCqHjk'
    return bdzb_url
# 合成url

import pandas as pd
import requests
import time  # 控制时间暂停
import random  # 产生随机数
import json



if __name__ == '__main__':
    # 创建表头
    final = pd.DataFrame(
        columns=(
            'num', 'name', 'lng', 'lat', 'address', 'province', 'city', 'area', 'detail', 'uid', 'geo_lng', 'geo_lat',
            'order'))
    ######################################
   # 输出表格
    final.to_csv('./step3_res.csv')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

    # 输入表格
    txt = pd.read_csv('./result_new.csv')  # 小区ID信息
    # txt['geo'] = 'x'  # 增加geo列

    f = open('./step3_res.csv', 'a', encoding='utf-8', newline='')
    writer = csv.writer(f)
    ##########################################

    for i in range(len(txt)):
        url = 'http://map.baidu.com/?pcevaname=pc4.1&qt=ext&ext_ver=new&l=12&uid=' + txt.loc[i, 'uid']
        wb_data = requests.get(url, headers=headers)  # 获取信息
        data = json.loads(wb_data.text)
        # 利用uid重新获取百度地图的对应数据，data

        try:
            num01 = data['content']['geo'].split('|1-')[1].replace(',', ';')
            geo = num01.split(';')
            b_url = bdzb_url(geo)
            # 获取边界需要的 url

            zb_data_wb = requests.get(b_url, headers=headers)  # 根据经纬度获取信息
            zb_data = json.loads(zb_data_wb.text)
            dd = zb_data['result']
            # 获取每个点对应的边界的结果 dd
            print(dd+'\n')

            # 写入每个点对应的边界点的行
            for j in range(len(dd)):
                writer.writerow([txt.at[i, 'num'], txt.at[i, 'name'], txt.at[i, 'lng'], txt.at[i, 'lat'],
                                 txt.at[i, 'address'], txt.at[i, 'province'], txt.at[i, 'city'], txt.at[i, 'area'],
                                 txt.at[i, 'detail'], txt.at[i, 'uid'],
                                 dd[j]['x'], dd[j]['y'], str(j + 1)])

            print(str(txt.loc[i, 'num']) + ',' + str(txt.loc[i, 'name']))

        # 如果搜索不到结果
        except:
            writer.writerow([txt.at[i, 'num'], txt.at[i, 'name'], txt.at[i, 'lng'], txt.at[i, 'lat'],
                             txt.at[i, 'address'], txt.at[i, 'province'],
                             txt.at[i, 'city'], txt.at[i, 'area'], txt.at[i, 'detail'], txt.at[i, 'uid'],
                             'x', 'y', str(0)])
            f.flush()
        time.sleep(random.uniform(1.0, 5.0))  # 随机休眠
    # 保存数据
    f.close()
