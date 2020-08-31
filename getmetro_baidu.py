import requests
import json
#from map_utils import coors_tencent_mercator_to_gcj02ll
import pandas as pd

# url='https://map.baidu.com/?qt=subways&c=131&format=json&t=1589545402711&callback=jsonp96324632'


url='https://map.baidu.com/?qt=subways&c={city_num}131&format=json&t=1589545402711'
res = requests.get(url=url)
print(res.text) 
json_data=json.loads(res.text)

 
with open('./data.json', 'w') as json_file:
    json_file.write(res.text)


def getdata(subway):
    list_data=[]
    for item in subway['l']:
        for stop in item['p']:
            if('uid' in stop['p_xmlattr']):
                uid=stop['p_xmlattr']['uid']
            else:
                uid=0
                print(stop['p_xmlattr'])
    #         print(uid)
            sid=stop['p_xmlattr']['sid']
            
            if(sid==''):
                continue
            px=stop['p_xmlattr']['px']
            py=stop['p_xmlattr']['py']
            ln=stop['p_xmlattr']['ln']
            #px,py=coors_tencent_mercator_to_gcj02ll([px,py])
            if('|' in ln):
                line=ln
                city='北京市'
            else:
                line=ln
                city='北京市'
            
            prod=[uid, city, line, sid, px, py]
            list_data.append(prod)
    return list_data

'''
import urllib.request
def get_record(url):
    resp = urllib.request.urlopen(url)
    ele_json = json.loads(resp.read())
    return ele_json
if __name__ == '__main__':
    print(get_record('http://abc.co/api/getall'))
'''

subway=json_data['subways']
list_data=getdata(subway)
column_name = ['id', '城市', '地铁线', '站名', 'px', 'py']
csv_name='data.xls'
xml_df = pd.DataFrame(list_data, columns=column_name)
xml_df.to_excel(csv_name, index=None) 