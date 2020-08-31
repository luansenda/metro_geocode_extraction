# -*- coding: utf-8 -*-
"""
Created on Thu May 14 16:48:11 2020

@author: senda
"""



import json
import requests
from lxml import etree

class Metro_gaode():

	def __init__(self, start_url=None):
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36"}

		self.start_url = 'http://map.amap.com/subway/index.html' if not start_url else start_url
		self.prefix_url = 'http://map.amap.com/service/subway?srhdata={}_drw_{}.json'

	# 首页获取所有区域名称
	def get_city(self):
		html = etree.HTML(requests.get(self.start_url, headers=self.headers).content)

		areas = html.xpath("//a[contains(@class, 'city')]")
		citys = {}
		for area in areas:
			citys[area.text] = (area.get('id'), area.get('cityname'))

		return citys

	def get_metro(self, city=None):
		citys = self.get_city()

		if city:
			id_name = citys.get(city, None)
			return {city : self.__get_metrolist(id_name)}
		else:
			result_dict = {}
			for city_name, id_name in citys.items():
				result_dict[city_name] = self.__get_metrolist(id_name)

			return result_dict

	def __get_metrolist(self, id_name):
		if id_name == None:
			return
		else:
			id, name = id_name
			url = self.prefix_url.format(id, name)

			result_list = []
			json_dict = json.loads(requests.get(url, headers=self.headers).text)

			metro_lines = json_dict.get("l")

			for line in metro_lines:
				line_name = line['kn']

				for station in line['st']:
					# 字段名为：地铁线路，站点名称，站点拼音，经度，纬度
					result_list.append((line_name, station['n'], station['sp'], *station['sl'].split(",")))
			return result_list

    
    
metro = Metro_gaode()  # 类 初始化
result_list = metro.get_metro("") # 如果不填区域名，则把所有的区域的地铁都爬取出来，类型为字典格式

import pandas as pd
# 定义各列
alldata = {}
city = []
line = []
station = []
pinyin = []
lat = []
lng = []

for city_name in result_list: # 遍历每个key值，即城市名
    for sub_list in result_list[city_name]: # 针对一个城市的列表，遍历每个站点
        city.append(city_name)
        line.append(sub_list[0])
        station.append(sub_list[1])
        pinyin.append(sub_list[2])
        lat.append(sub_list[3])
        lng.append(sub_list[4])

# 把每列合成字典
alldata['city'] = city
alldata['line'] = line
alldata['station'] = station
alldata['pinyin'] = pinyin
alldata['lat'] = lat
alldata['lng'] = lng
       
result=pd.DataFrame(alldata)#转dataframe
result.to_excel(r'C:\Users\g\Desktop\gaodemetro.xlsx',index=False)





















