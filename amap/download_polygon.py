# -*- encoding: utf-8 -*-
"""
@File    : download_polygon.py
@Time    : 2020/2/28 15:25
@Author  : GeoDoer
@Email   : geodoer@163.com
@Software: PyCharm
@Func   : 下载高德地图的面状数据
@Desc   : 以下载厦门小区数据为例
"""

import geopandas
from CrawlingGeoData.amap import poi
from CrawlingGeoData.amap import poiinfo

def amap_polygon(config):
    # 获得config["city"]内config["type"]类型的所有POI
    poi_out_fp = poi.amap_poi(config)
    if poi_out_fp is None: return None

    try:
        polygon_out_fp = config["polygon_out_fp"]
        gener_wgs84_shp = config.get("gener_wgs84_shp", False)
    except:
        print("参数解析失败")
        return None

    try:
        poi_gdf = geopandas.read_file(poi_out_fp)

    except:
        print("爬取错误")
        return None



if __name__ == '__main__':
    config = {
        "key": "efdaa20612fea6092643acd3c1fd7756",
        "city": "厦门",
        # "type" : None, #缺省为爬取所有类型
        "type": [  # 搜索的POI类型，缺省为爬取所有的类型
            # 可查看amap_poicode.xlsx查看类型
            ["商务住宅", "120000"]
        ],
        "save_field": ["id", "name", "type", "typecode", "address", "pname", "cityname"],  # 保存的字段。可选，默认为id、name
        "poi_out_fp": "厦门市商务住宅POI_gcj02.json",  # json格式
        "polygon_out_fp" : "厦门市商务住宅边界_gcj02.json", # json格式
        "gener_wgs84_shp" : True   # 生成WGS84的shp
    }
    amap_polygon(config)
    pass
