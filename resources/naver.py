from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error
from config import Config
import requests

class NaverSearchResource(Resource) :
    
    # 네이버 뉴스를 가져오는 API
    def get(self) :
        keyword = request.args.get('keyword')
        limit = request.args.get('limit')

        # 네이버 API를 호출
        # Restful Open API를 호출할때 사용하는 라이브러리 > requests 라이브러리

        data = {'query' : keyword, 'display' : limit}
        headers = {'X-Naver-Client-Id' : Config.NAVER_CLIENT_ID,
        'X-Naver-Client-Secret' : Config.NAVER_CLIENT_SECRET}

        response = requests.get('https://openapi.naver.com/v1/search/news.json', data, headers= headers)
        response = response.json()
        # print(response)
        
        # 뉴스 제목만 가져오기
        title_list = []
        for row in response['items'] :
            title_list.append(row['title'])

        return {'result' : 'success', 'items' : title_list}, 200

class NaverPapagoResource(Resource) :
    # 네이버 파파고 한국어 > 중국어 번역 API
    def post(self) :
        # {"content" : "안녕하세요~"}
        data = request.get_json()

        # 네이버 파파고 api 호출
        req_data = {'source' : 'ko', 'target' : 'zh-CN', 'text' : data['content']}
        headers = {'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Naver-Client-Id' : Config.NAVER_CLIENT_ID,
        'X-Naver-Client-Secret' : Config.NAVER_CLIENT_SECRET}

        response = requests.post('https://openapi.naver.com/v1/papago/n2mt', req_data, headers= headers)
        response = response.json()
        # print(response)

        # 번역된 결과 값 가져오기
        result_text = response['message']['result']['translatedText']

        return {'result' : 'success', 'result_text' : result_text}, 200