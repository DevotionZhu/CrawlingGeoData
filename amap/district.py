# -*- encoding: utf-8 -*-
"""
@File    : district.py
@Time    : 2020/2/24 17:12
@Author  : GeoDoer
@Email   : geodoer@163.com
@Software: PyCharm
@Func   : 获得行政区域查询
@Desc   : https://lbs.amap.com/api/webservice/guide/api/district
"""

import urllib.parse
import urllib.request
import json
from amap import tools

district_url = 'https://restapi.amap.com/v3/config/district'

'''
高德地图district接口：获得city的行政区边界
'''
def amap_district(config):
    '''
    :param
        config = {
            "key" : "4fac3db866dcc3b8a735651d3a7db1c7",
            "city" : "厦门"
        }
    :return:
    '''
    try:
        keywords = config["city"]
        key = config["key"]
    except:
        print("parameter error")
        return []

    try:
        param_json = {
            'key': key,
            'keywords': keywords,
            'extensions': 'all'
        }
        param_str = urllib.parse.urlencode(param_json)
        req_url = f'{district_url}?{param_str}'
    except:
        return []

    with urllib.request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
        obj = json.loads(data)
        if obj.get("status", '0') is not '1': return[]

        return obj.get("districts", [])

'''
得到city的四角边界
'''
def get_region(config):
    '''
    :param
        config = {
            "key" : "4fac3db866dcc3b8a735651d3a7db1c7",
            "city" : "厦门"
        }
    :return: minlng, maxlng, minlat, maxlat（最小经度，最大经度，最小纬度，最大纬度）
    '''
    try:
        disctrict = amap_district(config)

        bestresult = disctrict[0]
        polyline = bestresult.get("polyline", None)
        lines = tools.process_polyline_str(polyline)

        minlng, maxlng, minlat, maxlat = 200, -1, 200, -1
        for line in lines:
            for lng,lat in line:
                maxlng = max(lng, maxlng)
                minlng = min(lng, minlng)
                maxlat = max(lat, maxlat)
                minlat = min(lat, minlat)

        return minlng, maxlng, minlat, maxlat
    except:
        return []

if __name__ == '__main__':
    config = {
        "key" : "4fac3db866dcc3b8a735651d3a7db1c7",
        "city" : "厦门"
    }
    obj = get_region(config)
    print(obj)
    pass