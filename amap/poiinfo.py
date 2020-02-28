# -*- encoding: utf-8 -*-
"""
@File    : poiinfo.py
@Time    : 2020/2/28 12:01
@Author  : GeoDoer
@Email   : geodoer@163.com
@Software: PyCharm
@Func   : 高德地图的POI信息接口，可获得某个POI的矢量边界
@Desc   :
"""

import urllib.parse
from urllib import request
import json

poiinfo_url = "https://www.amap.com/service/poiInfo"

'''
高德数据POIINFO接口：针对线状数据
返回
'''
def amap_poiinfo_line(key, id):
    try:
        param_json = {
            # 关键参数
            "key" : key,
            "id" : id,
            # 其他参数
            "query_type" : "IDQ",
            "qii" : "true",
            "need_utd" : "true",
            "utd_sceneid" : "1000",
            "addr_poi_merge" : "true",
            "is_classify" : "true"
        }
        param_str = urllib.parse.urlencode(param_json)
        req_url = f'{poiinfo_url}?{param_str}'
        print(f"req: {req_url}")
    except:
        return None

    try:
        with request.urlopen(req_url) as f:
            ret = f.read()
            ret = ret.decode('utf-8')
            data = json.loads(ret)  # 将字符串转换为json
            # print(data)

            data = data['data']
            poi_list = data['poi_list'][0]
            domain_list = poi_list["domain_list"]
            for item in domain_list:
                name = item.get("name", None)
                value = item.get("value", None)
                if 'aoi' in name and value is not None:
                    # 有边界
                    pnt_arr = []
                    dataArr = [x.split('|') for x in value.split('_')]
                    for i in dataArr:
                        pnt = []
                        f = i[0].split(',')
                        pnt.append(float(f[0]))
                        pnt.append(float(f[1]))
                        pnt_arr.append(pnt)
                    return pnt_arr
            return None
    except:
        print("解析出错。")
        return None


'''
高德地图的POIINFO接口：针对面状数据
'''
def amap_poiinfo_polygon(key, id):
    try:
        param_json = {
            # 关键参数
            "key" : key,
            "id" : id,
            # 其他参数
            "query_type" : "IDQ",
            "qii" : "true",
            "need_utd" : "true",
            "utd_sceneid" : "1000",
            "addr_poi_merge" : "true",
            "is_classify" : "true"
        }
        param_str = urllib.parse.urlencode(param_json)
        req_url = f'{poiinfo_url}?{param_str}'
        print(f"req: {req_url}")
    except:
        return None

    try:
        with request.urlopen(req_url) as f:
            ret = f.read()
            ret = ret.decode('utf-8')
            data = json.loads(ret)  # 将字符串转换为json

            # 解析
            data = data['data']
            poi_list = data['poi_list'][0]
            domain_list = poi_list["domain_list"]
            for item in domain_list:
                name = item.get("name", None)
                value = item.get("value", None)
                if 'aoi' in name and value is not None:
                    # 有边界
                    pnt_arr = []
                    dataArr = [x.split('|') for x in value.split('_')]
                    for i in dataArr:
                        pnt = []
                        f = i[0].split(',')
                        pnt.append(float(f[0]))
                        pnt.append(float(f[1]))
                        pnt_arr.append(pnt)
                    return pnt_arr

            return None
    except:
        print("解析出错。")
        return None


'''
测试ID：
道路：B0FFGQ7PQK
小区：
    B0FFLAKSTK 无信息
    B02500TDTT 有信息
'''
if __name__ == '__main__':
    # 线状数据
    line = amap_poiinfo_line("efdaa20612fea6092643acd3c1fd7756", "B0FFGQ7PQK") # 线状矢量的ID
    print(line)

    # 面状数据
    polygon = amap_poiinfo_polygon("efdaa20612fea6092643acd3c1fd7756", "B0FFLAKSTK")
    print(polygon)
    polygon = amap_poiinfo_polygon("efdaa20612fea6092643acd3c1fd7756", "B02500TDTT")
    print(polygon)

    pass