from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from resources.naver import NaverPapagoResource, NaverSearchResource

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

api = Api(app)
api.add_resource(NaverSearchResource, '/news')
api.add_resource(NaverPapagoResource, '/chinese')


if __name__ == '__main__' :
    app.run()