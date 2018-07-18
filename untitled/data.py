# data
from xlrd import xlsx

region_id = list(range(1,4543))
region_name = ['']
region_id_name = dict(zip(region_id,region_name))

place_id = []
place_name = []
place_name_id = dict(zip(place_name,place_id))

poi_id = []
poi_cn_name = []
poi_id_name = dict(zip(poi_id,poi_cn_name))

login_url = ''
login_json = {"email":"","password":""}

search_url = ''

AREAS = {
    '关东': [],
    '关西': [],
    '九州': [],
    '北海道': [],
    '北岛': [],
    '南岛': [],
    '南法': [],
    '西西里岛': [],
    '托斯卡纳': [],
    '安达卢西亚': []
  }