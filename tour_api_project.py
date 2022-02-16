import pandas as pd
import json
import urllib.request
from os.path import basename

client_id = "cTWUGiJR/GRNsWP1Zvpr6EfojgF2NzRo6pzKHUXZplHewa1M8A9dkuiqnqsbVFTvix8hc8GWw4abmLFx7YB5tA=="
# 공공데이터포탈 api 인증키

def getRequestUrl(url): # 서버에 요청하는 함수

    req = urllib.request.Request(url)  # 서버에 보낼 요청객체를 생성

    try:
        response = urllib.request.urlopen(req)  # 서버에 요청객체 req를 전달하여 응답을 받아 response에 저장
        if response.getcode() == 200:  # 응답코드가 200이면
            print('호출성공')
            ret = response.read().decode('utf-8')
            return ret
    except:
        # print('Error Code :', response.getcode())
        # print('에러발생 주소:', url)
        print('더이상 가져올 데이터가 없거나 호출에 에러가 발생했습니다.')
        return None


def getTourismStatsItem(yyyymm, nat_code, ed_cd): # url 만들어주는 함수
    baseUrl = "http://openapi.tour.go.kr/openapi/service"  # 기본 API 주소
    service_url = baseUrl + '/EdrcntTourismStatsService' + '/getEdrcntTourismStatsList' # + 서비스명 + 오퍼레이션명
    # params ={'serviceKey' : '서비스키', 'YM' : '201201', 'NAT_CD' : '112', 'ED_CD' : 'D' } 사이트샘플코드
    # + 파라미터값
    params1 = "?serviceKey=" + client_id
    params2 = "&YM=" + yyyymm # 월단위
    params3 = "&NAT_CD=" + nat_code
    params4 = "&ED_CD=" + ed_cd
    params5 = "&_type=json"

    url = service_url + params1 + params2 + params3 + params4 + params5


    responseDecode = getRequestUrl(url)  # 호출 성공 시 디코딩된 응답 데이터를 저장
    if (responseDecode) == None: # 에러가 났을 때
        return None
    else:
        return json.loads(responseDecode)


def getTourismStatsService(nat_code, ed_cd, nStartYear, nEndYear):  # 월 데이터 요청

    data_flag = 0
    jsonResult = []
    return_list = []

    for year in range(nStartYear,nEndYear+1):
        for month in range(1,13): # for(i=0;i<13;i++)
            if data_flag == 1:
                break
            yyyymm = "{0}{1:0>2}".format(year,month) # yyyy01 ~yyyy12 형식변환
            jsonData = getTourismStatsItem(yyyymm,nat_code,ed_cd)
            # print(jsonData)
            if jsonData['response']['body']['items'] == '': # 제이슨데이타 안에 레스폰스 안에 바디 안에 아이템스
                data_flag = 1
                print('데이터가 끝났습니다.')
                print("출력데이터는 {0}년 {1}월 전까지 데이터입니다".format(year,month))
                break

            natName = jsonData['response']['body']['items']['item']['natKorNm'] # 국가이름 추출
            num = jsonData['response']['body']['items']['item']['num'] # 방한외국관광객 수 추출
            # ed = jsonData['response']['body']['items']['item']['ed'] # 방한외국관광객

            jsonResult.append({'nat_Name':natName,'nat_cd':nat_code,'yyyymm':yyyymm, 'visit_cnt':num})
            return_list.append([natName,nat_code,yyyymm,num])

    return (jsonResult, return_list,natName)


# input 추가
# 국가는 3개 중 선택(중국:112, 일본:130, 미국:275)
# 몇년(시작 년도)부터 몇년(끝나는 년도)까지 출력할 것인지?

print("1.중국:112, 2.일본:130, 3.미국:275")
nat_num = input("내한관광객수를 알고 싶은 국가를 선택하세요.")
if nat_num == '1':
    nat_code = 112
elif nat_num == '2':
    nat_code = 130
if nat_num == '3':
    nat_code = 275

print("몇년부터 몇년까지 출력할까요?")
start_year = input("시작년도")
end_year = input("끝나는 년도")
jsonResult, return_result, nat_name = getTourismStatsService(str(nat_code), 'E', int(start_year), int(end_year))

# print(jsonResult)
# print(return_result)
# print(nat_name)

result_df=pd.DataFrame(return_result, columns=['입국자코드','국가코드','입국날짜','입국자수'])
result_df.to_csv('[%s]내한관광통계.csv' % nat_name, index=False, encoding='cp949')