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
import os
import time
from amap import tools
from amap import poi
from amap import poiinfo
from shapely.geometry import Polygon

def amap_polygon(config):
    try:
        key = config["key"]
        polygon_out_fp = config["polygon_out_fp"]
        poi_out_fp = config["poi_out_fp"]
        out_dir = config.get("out_dir", None)
    except:
        print("参数解析失败")
        return None

    if out_dir is not None:
        polygon_out_fp = os.path.join(out_dir, polygon_out_fp)
        poi_out_fp = os.path.join(out_dir, poi_out_fp)
        config["poi_out_fp"] = poi_out_fp

    # 获得config["city"]内config["type"]类型的所有POI
    if not os.path.exists(poi_out_fp):
        if poi.amap_poi(config) is None: #生成poi文件
            return None

    # 获取边界信息
    try:
        # POI数据
        poi_gdf = geopandas.read_file(poi_out_fp)

        # 存储polygon_gdf
        column_name = poi_gdf.columns.values
        attr = {}
        for key in column_name:
            attr[key] = []
        geoms = []

        no_poly_cnt = 0
        for i in range(0, len(poi_gdf)):
            id = poi_gdf.iloc[i]["id"]
            poly = poiinfo.amap_poiinfo_polygon(key, id)

            print("sleep 2s")
            time.sleep(2)  # 每一个间隔2s

            if poly is None:
                no_poly_cnt += 1
                print(f"{no_poly_cnt}个POI没有边界信息")
                continue

            geoms.append( Polygon(poly) )
            for key in column_name:
                attr[key].append( poi_gdf.iloc[i][key] )

            if i%2==0:
                gdf = geopandas.GeoDataFrame(
                    attr,
                    geometry=geoms
                )
                gdf.to_file(polygon_out_fp, driver='GeoJSON', encoding="utf-8")
                print(f"共找到{len(geoms)}/{len(poi_gdf)}个边界信息")

                print("sleep 5s")
                time.sleep(5) #每2个间隔5s

        gdf = geopandas.GeoDataFrame(
            attr,
            geometry=geoms
        )
        gdf.to_file(polygon_out_fp, driver='GeoJSON', encoding="utf-8")
        print(f"共找到{len(geoms)}/{len(poi_gdf)}个边界信息")
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
        "out_dir" : r"D:\mycode\CrawlingGeoData\data", # 可选
        "poi_out_fp": "厦门市商务住宅POI_gcj02.json",  # json格式
        "polygon_out_fp" : "厦门市商务住宅边界_gcj02.json", # json格式
    }
    amap_polygon(config) # 爬取面状的边界信息
    # tools.PntGeoJSONToShp_WGS84(os.path.join(config["out_dir"], config["poi_out_fp"]) )  # 转成shp文件，并把坐标系从火星坐标转到WGS84
    tools.PolygonGeoJSONToShp_WGS84(os.path.join(config["out_dir"], config["polygon_out_fp"]) )# 转成shp文件，并把坐标系从火星坐标转到WGS84

    pass
