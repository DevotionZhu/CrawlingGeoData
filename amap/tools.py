# -*- encoding: utf-8 -*-
"""
@File    : tools.py
@Time    : 2020/2/26 9:54
@Author  : GeoDoer
@Email   : geodoer@163.com
@Software: PyCharm
@Func   :
@Desc   :
"""

import xlrd
import geopandas

def process_polyline_str(polyline_str):
    try:
        lines_str = polyline_str.split('|')
        lines = []
        for line_str in lines_str:
            line = []
            lnglats = line_str.split(';')
            for lnglat in lnglats:
                lng,lat = lnglat.split(',')
                line.append(
                    ( float(lng), float(lat)  )
                )
            lines.append(line )
        return lines
    except:
        return []

"""
根据范围划分网格，获得每个网格的四边形边界
返回：经度和纬度用","分割，经度在前，纬度在后，坐标对用"|"分割。经纬度小数点后不得超过6位
    多边形为矩形时，可传入左上右下两顶点坐标对；其他情况下首尾坐标对需相同。
"""
def generalID(region, col_num, row_num):
    minlng, maxlng, minlat, maxlat = region

    polylists = []
    lat_step = (maxlat - minlat) / row_num
    lng_step = (maxlng - minlng) / col_num

    for r in range(row_num):
        for c in range(col_num):
            left_lng = minlng + lng_step * c
            right_lng = minlng + lng_step * (c+1)
            down_lat = minlat + lat_step * r
            up_lat = minlat + lat_step * (r+1)
            # 经度lng在前，纬度lat在后。左上右下两顶点坐标对
            poly_str = f"{left_lng},{up_lat}|{right_lng},{down_lat}"
            polylists.append(poly_str)
    return polylists


#读取所有的type以及typename
"""
读取amap的所有type以及typename
"""
def get_all_type(fp='amap_poicode.xlsx'):
    '''
        typename = "道路名"
        types = '190301'
        typename以及types在高德提供的相关文档中下载，https://lbs.amap.com/api/webservice/download
    :return:
    '''
    myWordbook = xlrd.open_workbook(fp)
    mySheets = myWordbook.sheets()
    mySheet = mySheets[2]
    # 获取列数
    nrows = mySheet.nrows
    typelist = []
    for i in range(1, nrows):
        tmp = []
        tmp.append(mySheet.cell_value(i, 4))
        tmp.append(mySheet.cell_value(i, 1))
        typelist.append(tmp)
    return typelist

def PntGeoJSONToShp_WGS84(json_fp, shp_fp=None): #点状GeoJSON文件转成SHP（火星坐标 转 WGS84）
    from CrawlingGeoData.amap import coordinate_conversion
    from shapely.geometry import point

    if not json_fp.endswith("json"): return False

    if shp_fp is None:
        shp_fp = "{}_wgs84.shp".format(json_fp[:-5])
    elif not shp_fp.endswith("shp"):
        return False

    gdf = geopandas.read_file(json_fp)
    # GCJ02转WGS84
    for i in range(0, len(gdf)):
        geom = gdf.geometry[i]  # 获取空间属性，即GeoSeries
        lng,lat = geom.x, geom.y  # x=117.967657, y=24.472853
        lng,lat = coordinate_conversion.gcj02towgs84(lng, lat)
        gdf.geometry[i] = point.Point(lng, lat)

    # 设置成WGS84，并保存
    gdf.crs = {'init' :'epsg:4326'}
    gdf.to_file(shp_fp, encoding="utf-8")
    return shp_fp

def GeoJSONToShp(json_fp, shp_fp=None):
    if not json_fp.endswith("json"): return False

    if shp_fp is None: shp_fp = "{}.shp".format( json_fp[:-5] )
    elif not shp_fp.endswith("shp"): return False

    gdf = geopandas.read_file(json_fp)
    gdf.to_file(shp_fp, encoding="utf-8")
    return shp_fp

if __name__ == '__main__':
    json_fp = r"D:\mycode\PythonGIS\CrawlingGeoData\amap\厦门市小区POI_gcj02.json"
    GeoJSONToShp(json_fp)
    PntGeoJSONToShp_WGS84(json_fp)
    pass