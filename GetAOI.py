# 爬取AOI 原始
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


# import pandas as pd
import requests
import time  # 控制时间暂停
import random  # 产生随机数
import json
import pandas as pd


if __name__ == '__main__':
    # final1 = pd.DataFrame(
    #     columns=('num', 'name', 'lng', 'lat', 'address', 'province', 'city', 'area', 'detail', 'uid', 'geo_lng', 'geo_lat', 'order'))
    # final1.to_csv(r'./step3_res.csv', mode='a', header=True, index=False)
    # 创建表头
    final = pd.DataFrame(
        columns=(
        'num', 'name', 'lng', 'lat', 'address', 'province', 'city', 'area', 'detail', 'uid', 'geo_lng', 'geo_lat',
        'order'))

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

    txt = pd.read_csv('./result_new.csv')  # 小区ID信息
    # txt.drop(columns=['num'])
    txt['geo'] = 'x'  # 增加geo列

    f = open('./step3_res_4.csv', 'a', encoding='utf-8', newline='')
    writer = csv.writer(f)

    for i in range(7341, len(txt)):
        final.at[i, 'num'] = txt.loc[i, 'num']
        final.at[i, 'name'] = txt.loc[i, 'name']
        final.at[i, 'lng'] = txt.loc[i, 'lng']
        final.at[i, 'lat'] = txt.loc[i, 'lat']
        final.at[i, 'address'] = txt.loc[i, 'address']
        final.at[i, 'province'] = txt.loc[i, 'province']
        final.at[i, 'city'] = txt.loc[i, 'city']
        final.at[i, 'area'] = txt.loc[i, 'area']
        final.at[i, 'detail'] = txt.loc[i, 'detail']
        final.at[i, 'uid'] = txt.loc[i, 'uid']

        url = 'http://map.baidu.com/?pcevaname=pc4.1&qt=ext&ext_ver=new&l=12&uid=' + txt.loc[i, 'uid']
        wb_data = requests.get(url, headers=headers)  # 获取信息
        data = json.loads(wb_data.text)
        # 利用uid重新获取百度地图的对应数据，data

        try:
            num01 = data['content']['geo'].split('|1-')[1].replace(',', ';')
            geo = num01.split(';')
            b_url = bdzb_url(geo)
            # 获取边界需要的 url

            zb_data_wb = requests.get(b_url, headers=headers)  # 获取信息
            zb_data = json.loads(zb_data_wb.text)
            dd = zb_data['result']
            # 获取每个点对应的边界的结果 dd

            for j in range(len(dd)):
                writer.writerow([final.at[i, 'num'], final.at[i, 'name'], final.at[i, 'lng'], final.at[i, 'lat'],
                                 final.at[i, 'address'], final.at[i, 'province'], final.at[i, 'city'],
                                 final.at[i, 'area'], final.at[i, 'detail'], final.at[i, 'uid'],
                                 dd[j]['x'], dd[j]['y'], str(j + 1)])

                # temp = final
                # temp.at[i, 'geo_lng'] = dd[j]['x']
                # temp.at[i, 'geo_lat'] = dd[j]['y']
                # temp.to_csv(r'./step3_res.csv', mode='a', header=False, index=False)

            # txt.loc[i, 'geo'] = str(zb_data['result'])
            print(str(txt.loc[i, 'num']) + ',' + str(txt.loc[i, 'name']))
        except:
            # txt.loc[i, 'geo'] = 'x'
            final.at[i, 'geo_lng'] = 'x'
            final.at[i, 'geo_lat'] = 'y'
            # writer.writerow([final.at[i, 'num'], final.at[i, 'name'], final.at[i, 'lng'], final.at[i, 'lat'],
            # final.at[i, 'address'], final.at[i, 'province'],
            # final.at[i, 'city'], final.at[i, 'area'], final.at[i, 'detail'], final.at[i, 'uid'],
            # final.at[i, 'geo_lng'], final.at[i, 'geo_lat'], str(0)])
            f.flush()
            # final.to_csv(r'./step3_res.csv', mode='a', header=False, index=False)

        # final.to_csv(r'./step3_res.csv', mode='a', header=False, index=False)
        time.sleep(random.uniform(0.5, 2.0))  # 随机休眠
    # 保存数据
    f.close()
    # final.to_csv(r'./step3_res.csv', index=False)
    # txt.to_csv(r'./step3_res.csv', index=False)
