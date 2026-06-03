import json
import codecs
import os
import urllib.request
# import imp
import time

# reload(sys)
# sys.setdefaultencoding('utf8')
# 复制的按矩形检索的方法，还未尝试

class BaiDuPOI(object):
    def __init__(self, itemy, loc):

        self.itemy = itemy
        self.loc = loc


    def urls(self):
        api_key = baidu_api
        urls = []
        for pages in range(0, 20):
            # convert_cont = urllib.request.quote(self.itemy)
            url = 'http://api.map.baidu.com/place/v2/search?query=' + urllib.request.quote(self.itemy) + '&bounds=' + self.loc + '&page_size=20&page_num=' + str(
                pages) + '&output=json&ak=' + api_key
            urls.append(url)
        return urls


    def baidu_search(self):
        json_sel = []
        for url in self.urls():
            json_obj = urllib.request.urlopen(url)
            data = json.load(json_obj)
            for item in data['results']:
                jname = item["name"]
                jlat = item["location"]["lat"]
                jlng = item["location"]["lng"]
                js_sel = jname + ',' + str(jlat) + ',' + str(jlng)
                json_sel.append(js_sel)
        return json_sel


class LocaDiv(object):
    def __init__(self, loc_all):
        self.loc_all = loc_all

    def lat_all(self):
        lat_sw = float(self.loc_all.split(',')[0])
        lat_ne = float(self.loc_all.split(',')[2])
        lat_list = []
        for i in range(0, int((lat_ne - lat_sw + 0.0001) / 0.1)):  # 0.1为网格大小，可更改
            lat_list.append(lat_sw + 0.1 * i)  # 0.05
        lat_list.append(lat_ne)
        return lat_list


    def lng_all(self):
        lng_sw = float(self.loc_all.split(',')[1])
        lng_ne = float(self.loc_all.split(',')[3])
        lng_list = []
        for i in range(0, int((lng_ne - lng_sw + 0.0001) / 0.1)):  # 0.1为网格大小，可更改
            lng_list.append(lng_sw + 0.1 * i)  # 0.1为网格大小，可更改
        lng_list.append(lng_ne)
        return lng_list


    def ls_com(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ab_list = []
        for i in range(0, len(l1)):
            a = str(l1[i])
            for i2 in range(0, len(l2)):
                b = str(l2[i2])
                ab = a + ',' + b
                ab_list.append(ab)
        return ab_list


    def ls_row(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ls_com_v = self.ls_com()
        ls = []
        for n in range(0, len(l1) - 1):
            for i in range(0 + len(l1) * n, len(l2) + (len(l2)) * n - 1):
                a = ls_com_v[i]
                b = ls_com_v[i + len(l2) + 1]
                ab = a + ',' + b
                ls.append(ab)
        return ls

if __name__ == '__main__':
# ak
    baidu_api = "w9HGFgmL64By3EbCf8ukfEIwx4uCqHjk"  # 这里填入你的百度API的ak
    print
    "开始爬取数据，请稍等..."
    start_time = time.time()
    loc = LocaDiv('31.902451,118.570731,32.248064, 119.084131')
    locs_to_use = loc.ls_row()

    for loc_to_use in locs_to_use:
        par = BaiDuPOI(u'医疗', loc_to_use)  # 请修改爬取的类别
        a = par.baidu_search()
        doc = open('医疗保健.csv', 'a+')
        doc.write(codecs.BOM_UTF8)
        for ax in a:
            doc.write(ax)
            doc.write('\n')
        doc.close()
    end_time = time.time()
    print("购物爬取完毕，用时%.2f秒" % (end_time - start_time))
