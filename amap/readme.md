高德地图API文档：https://lbs.amap.com/api/webservice/guide/api/search


## 接口列表

| | 说明 | 相关文章 |
| - | - | - |
| 行政区边界 |  | [官方说明](lbs.amap.com/api/webservice/guide/api/district)<Br/>
| POI搜索 | 用于搜索周边的地物 | [搜索POI官方说明](https://lbs.amap.com/api/webservice/guide/api/search)
| 根据POI的ID查询地物 | ditu.amap.com/detail/get/detail?id=B0FFHVEECG |
| 根据POI的ID查找边界信息 |  https://gaode.com/service/poiInfo?query_type=IDQ&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=11&id=B022F0071G&city=341003 |

## 说明
1. 所有接口爬取的坐标标准为GCJ-02火星坐标，并且都保存成GeoJSON格式
2. 想要转成shp文件，并转成WGS84坐标系，可调用tools.py文件中的函数

## 爬取策略
##### 爬取POI
实现：poi.py
步骤：

1. 根据“行政区边界”获得研究区的范围
2. 将研究区分割成多个四边形小方格
3. 读取高德地图POI所有的type和typename
4. 对每个小方格进行获取

#### 爬取线状地物
实现：download_line.py


#### 爬取线状地物
示例结果：WGS84坐标系结果 与 高清影像贴合

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200228231238493.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

实现：download_polygon.py
步骤：

1. 设置爬取参数，获取POI
2. 根据POI ID获取边界

注意：
1. 有些POI没有矢量边界
2. 生成的为火星坐标的GeoJSON文件，若要转成WGS84坐标系，或生成JSON，可使用tools.py中的函数
3. 还未做反爬策略

## Github相关项目
1. https://blog.csdn.net/weixin_40902527/article/details/85759232
2. https://github.com/Accright/java-map-spider 获取高德和百度地图的POI及边界数据爬虫-JAVA版本
3. https://github.com/tonychen257/-POI- 里面包含了高德地图POI爬取，百度高德渔网点爬取