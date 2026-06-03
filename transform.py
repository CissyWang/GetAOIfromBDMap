import math
import pandas as pd
# 坐标转化计算 不如插件标准

pi = 3.141592653589793234
r_pi = pi * 3000.0 / 180.0
la = 6378245.0
ob = 0.00669342162296594322


def transformlat(lon, lat):
    r = -100.0 + 2.0 * lon + 3.0 * lat + 0.2 * lat * lat + 0.1 * lon * lat + 0.2 * math.sqrt(math.fabs(lon))
    r += (20.0 * math.sin(6.0 * lon * pi) + 20.0 * math.sin(2.0 * lon * pi)) * 2.0 / 3.0
    r += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    r += (160.0 * math.sin(lat / 12.0 * pi) + 320.0 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return r


def transformlng(lon, lat):
    r = 300.0 + lon + 2.0 * lat + 0.1 * lon * lon + 0.1 * lon * lat + 0.1 * math.sqrt(math.fabs(lon))
    r += (20.0 * math.sin(6.0 * lon * pi) + 20.0 * math.sin(2.0 * lon * pi)) * 2.0 / 3.0
    r += (20.0 * math.sin(lon * pi) + 40.0 * math.sin(lon / 3.0 * pi)) * 2.0 / 3.0
    r += (150.0 * math.sin(lon / 12.0 * pi) + 300.0 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return r


# 在中国返回false
def judge_China(lon, lat):
    if lon < 70 or lon > 140:
        return True
    if lat < 0 or lat > 55:
        return True
    return False

def bd09_gcj02(lon_bd09,lat_bd09):
    m = lon_bd09 - 0.0065
    n = lat_bd09 - 0.006
    c = math.sqrt(m * m +n * n) - 0.00002 * math.sin(n * r_pi)
    o = math.atan2(n,m) - 0.000003 * math.cos(m * r_pi)
    lon_gcj02 = c* math.cos(o)
    lat_gcj02 = c* math.sin(o)
    return[lon_gcj02, lat_gcj02]

def bd09_wgs84(lon_bd09,lat_bd09):
    tmpList_gcj02 = bd09_gcj02(lon_bd09,lat_bd09)

    return gcj02_wgs84(tmpList_gcj02[0],tmpList_gcj02[1])
def gcj02_wgs84(lon_gcj02, lat_gcj02):
    if judge_China(lon_gcj02, lat_gcj02):
        return [lon_gcj02, lat_gcj02]
    tlat = transformlat(lon_gcj02 - 105.0, lat_gcj02 - 35.0)
    tlng = transformlng(lon_gcj02 - 105, lat_gcj02 - 35.0)
    rlat = lat_gcj02 / 180.0 * pi
    m = math.sin(rlat)
    m = 1 - ob * m * m
    sm = math.sqrt(m)
    tlat = (tlat * 180.0) / ((la * (1 - ob)) / (m * sm) * pi)
    tlng = (tlng * 180.0) / (la / sm * math.cos(rlat) * pi)
    lat_wgs84 = 2 * lat_gcj02 - (lat_gcj02 + tlat)
    lon_wgs84 = 2 * lon_gcj02 - (lon_gcj02 + tlng)
    return [lon_wgs84, lat_wgs84]


if __name__ == '__main__':
    filename = 'result_new.csv'
    path = 'E:\\BigData\\小区aoi\\' + filename
    data = pd.read_csv(path)
    final = data.copy()

    for i in range(len(data)):
        lon = data.loc[i, 'lng']
        lat = data.loc[i, 'lat']

        if judge_China(lon, lat):
            continue
        else:
            # lonlat = gcj02_wgs84(lon, lat)
            lonlat = bd09_wgs84(lon, lat)
            final.loc[i, 'lng'] = lonlat[0]
            final.loc[i, 'lat'] = lonlat[1]

    final.to_csv(r'./transform.csv', mode='a', header=True, index=False)
