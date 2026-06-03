import requests, re, xlwt, datetime
from bs4 import BeautifulSoup
import pandas as pd
import csv
# 爬取网页信息

# 初始化
def init():
    global url, province_name, headers
    url = 'http://www.yixue.com/'
    province_name = '南京市'
    headers = {
        'Host': 'www.yixue.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }


# 存储数据


def sav_message(messgae):
    final = pd.DataFrame(columns=("医院名称", "医院地址", "联系电话", "医院等级", "重点科室", "经营方式", "传真号码", "电子邮箱", "医院网站"))
    i = 0
    for data in messgae[7]:
        try:
            final.at[i, '医院名称'] = data.b.a.text
            textData = data.text.split('\n')
            for data_1 in textData:
                now_data = data_1.split('：')
                print(now_data)

                for tittle in final.columns:
                    if tittle == now_data[0]:
                        final.at[i, tittle] = now_data[1]


        except:
            print('404')

        i = i + 1

    print(final)
    final.to_csv("E:\BigData\hospital_f1.csv")


def sav_message1(message, message1):
    final = pd.DataFrame(columns=("医院名称", "医院地址", "联系电话", "医院等级", "重点科室", "经营方式", "传真号码", "电子邮箱", "医院网站"))
    j = 0
    for data in message1[4]:
        datanew = data.text.split('\n')
        if datanew is not None :
            final.at[j, '医院名称'] = datanew[0]
            j += 1

        else:
             print("null")

    i = 0
    for data in message[7]:
        try:
            datanew = data.text.split('\n')
            if datanew[0] == final.at[i, '医院名称']:
                textData = data.text.split('\n')
                print(textData)
                for data_1 in textData:
                    now_data = data_1.split('：')
                    print(now_data)

                    for tittle in final.columns:
                        if tittle == now_data[0]:
                            final.at[i, tittle] = now_data[1]
                i = i + 1

        except:
            print('404')



    print(final)
    # final.to_csv("E:\BigData\hospital_f2.csv")


# 获取当前省数据
# def get_province_hospital(province_now):
#     r = requests.get(url + province_now + '医院列表', headers=headers, timeout=10)
#     soup = BeautifulSoup(r.text, "lxml")
#
#     message = soup.find_all('ul')
#     sav_message(message, province_now)


# 主函数
if __name__ == '__main__':
    init()
    # for province in province_name:
    #     try:
    # get_province_hospital(province)
    r = requests.get(url + province_name + '医院列表', headers=headers, timeout=10)
    r1 = requests.get(url + province_name + '综合医院列表', headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "lxml")
    message = soup.find_all('ul')
    soup1 = BeautifulSoup(r1.text, "lxml")
    message1 = soup1.find_all('ul')

    sav_message1(message,message1)
    # except:
    #     print('notfound')
