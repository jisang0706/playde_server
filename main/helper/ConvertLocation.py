import my_settings
import requests

GC_API_URL = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?'
GC_BASE_URL = GC_API_URL + 'X-NCP-APIGW-API-KEY-ID=' + my_settings.Geocode.client_id + '&' +\
              'X-NCP-APIGW-API-KEY=' + my_settings.Geocode.client_secrit + '&'

RGC_API_URL = 'https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc?'
RGC_BASE_URL = RGC_API_URL + 'X-NCP-APIGW-API-KEY-ID=' + my_settings.Geocode.client_id + '&' +\
              'X-NCP-APIGW-API-KEY=' + my_settings.Geocode.client_secrit + '&'

def latlng_to_address(coords):
    response = requests.get(RGC_BASE_URL + 'coords=' + str(coords[0]) + ',' + str(coords[1]) + '&output=json&orders=legalcode')
    if response.status_code != 200: return 'ERROR'

    dic = response.json()
    if dic['status']['code'] == 0:
        area1 = dic['results'][0]['region']['area1']['name']
        area2 = dic['results'][0]['region']['area2']['name']
        area3 = dic['results'][0]['region']['area3']['name']
        return area1, area2, area3
    else:
        return 'ERROR', 0, 0

def address_to_latlng(address):
    response = requests.get(GC_BASE_URL + 'query=' + address)
    if response.status_code != 200: return 'ERROR'

    dic = response.json()
    coords = [dic['addresses'][0]['x'], dic['addresses'][0]['y']]
    return coords
