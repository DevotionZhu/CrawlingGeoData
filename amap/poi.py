# -*- encoding: utf-8 -*-
"""
@File    : amap_poi.py
@Time    : 2020/2/24 15:14
@Author  : GeoDoer
@Email   : geodoer@163.com
@Software: PyCharm
@Func   : 获取矩形内的所有POI的id,name,location（经纬度坐标）,adname（所属区），并将爬取的数据存入json文件中（未去重）
@Desc   : 官方说明文档：http://lbs.amap.com/api/webservice/guide/api/search
            示例：https://restapi.amap.com/v3/place/polygon?key=e28ed3ab9b8b955626b7a0247d6cea68&polygon=120.856804,30.675593|121.856804,31.675593&keywords="道路名"&types=190301&offset=20&page=1&extensions=all
"""

import urllib.parse
from urllib import request
import json
from CrawlingGeoData.amap import tools
from CrawlingGeoData.amap import district
from shapely.geometry import point
import geopandas
import os

search_url = 'https://restapi.amap.com/v3/place/polygon'

"""
高德地图POI服务
https://lbs.amap.com/api/webservice/guide/api/search#polygon
"""
def amap_poi(config):
    try:
        key = config["key"]                     # 高德地图的Key
        city = config["city"]                   # 城市
        save_fp = config["poi_out_fp"]          # 存储路径
        region = district.get_region(config)    # 区域范围

        # 爬取的字段
        save_field = config.get("save_field", ["id", "name"] )

        # 爬取的类型
        typenametypes = config.get("type", None)    #示例：[['汽车服务相关', '010000'], ['加油站', '010100'], ... ]
        if typenametypes is None: #缺省则爬取所有的类型
            typenametypes = tools.get_all_type()


        # 将矩形分成row_num行、col_num列的小矩阵
        col_num = config.get("col_num", 4)
        row_num = config.get("row_num", 4)
    except:
        print("parameter error")

    try:
        # 爬取结果
        attr = {}   # 属性
        geom = []   # 坐标
        for field in save_field: #初始化保存的字段
            attr[field] = []

        # 将矩形拆分成col_num，row_num的小方块
        polylist = tools.generalID(region, col_num, row_num)
        # 边爬边存
        poinum = 0  #POI个数
        polynum = 1 #方格
        for polygon in polylist:
            print(f"正在第{polynum}个方格区搜索")
            for typenametype in typenametypes:
                pois = get_pois(key, polygon, typenametype[0], typenametype[1])
                for poi in pois:
                    if city not in poi["cityname"]: #不是该城市的POI
                        continue

                    poinum += 1
                    # 坐标（高德地图为火星坐标）
                    location_str = poi["location"]
                    tmp = location_str.split(',')
                    pnt = point.Point(float(tmp[0]), float(tmp[1]))
                    geom.append(pnt)
                    # 属性
                    for field in save_field:
                        value = poi.get(field, "")
                        attr[field].append( str(value) )

                    # 500个数据存一次文件
                    num_of_per_time = config.get("number_of_per_time", 500) #每一次存储到文件的数据量
                    if poinum % num_of_per_time==0:
                        gdf = geopandas.GeoDataFrame(
                            attr,
                            geometry= geom
                        )
                        gdf.to_file(save_fp, driver='GeoJSON', encoding="utf-8")

            polynum += 1
        # 保存
        gdf = geopandas.GeoDataFrame(
            attr,
            geometry=geom
        )
        gdf.to_file(save_fp, driver='GeoJSON', encoding="utf-8")
        return save_fp
    except:
        return None

"""
获取polygon内的所有数据
"""
def get_pois(key, polygon, typename, types):
    i = 1
    all_pages = []
    while True:
        results = get_page_poi(key, polygon, typename, types, i)
        if results == []:
            break
        all_pages += results
        i += 1
    return all_pages


"""
获取每一页的数据
"""
def get_page_poi(key, polygon, typename, types, page):
    try:
        param_json = {
            "key" : key,
            'polygon' : polygon,  #左上右下两顶点坐标对
            "keywords" : typename,
            "types" : types,
            "offset" : str(20),
            "page" : str(page),
            "extensions" : "all",
            "output" : "json"
        }
        param_str = urllib.parse.urlencode(param_json)
        req_url = f'{search_url}?{param_str}'
        print(f"req: {req_url}")
    except:
        return []

    with request.urlopen(req_url) as f:
        ret = f.read()
        ret = ret.decode('utf-8')
        data = json.loads(ret)  # 将字符串转换为json
        if data.get('pois') != None:
            pois = data['pois']
            return pois

    return []

if __name__ == '__main__':
    config = {
        "key": "efdaa20612fea6092643acd3c1fd7756",
        "city" : "厦门",
        # "type" : None, #缺省为爬取所有类型
        "type" : [ #搜索的POI类型，缺省为爬取所有的类型
            # 可查看amap_poicode.xlsx查看类型
            ["商务住宅", "120000"]
        ],
        "save_field" : ["id", "name", "type", "typecode", "address", "pname", "cityname"], #保存的字段。可选，默认为id、name
        "poi_out_fp": "厦门市商务住宅POI_gcj02.json" #json格式
    }
    amap_poi(config)
    tools.PntGeoJSONToShp_WGS84(config["poi_out_fp"]) #转成shp文件，并把坐标系从火星坐标转到WGS84
    pass