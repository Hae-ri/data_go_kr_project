import requests
from urllib import parse # 파싱=데이터를 쪼개는 것

base_url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/'
api_key = 'UwqEYc9kfsk2s1L6iBtrPDSOc0jCkWgX/MoLS62ZBsYUwkEPpzaQCsOocjVnDzGsW1LQbqnX5YUEaLbEyKI1gg=='

url_holiday= base_url + 'getRestDeInfo'

params = {'serviceKey':api_key,
          'solYear':2022,
          'numOfRows': 100}

response = requests.get(url_holiday, params)
print(response.text) 

