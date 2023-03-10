# Flask 앱을 만들기 위해 flask 모듈을 참조
# 플라스크 APP을 초기화 하는 함수를 만듭니다. 인자는 __name__ 변수
# __name__ 은 현재 __name__이 작성된 파일명을 문자열로 저장하고 있거나 __main__이란 문자열 값을 저장
from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
# 로그인이 필요할 때 redirect(or redirection)할 view를 설정
from flask_login import LoginManager
client = MongoClient('mongodb+srv://joonyeol:1234@sparta.afgjtfy.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


# app.config은 생성될 app의 비밀 키 값, 암호화에 사용되는 값이니 유출 금지
def create_app():
    app = Flask(__name__)
    app.secret_key = 'nebecamp-miniproject-8team'


# main.py로 ㄱㄱ


    # views에서 블루프린트 인스턴스 가져오기 및 플라스크 앱에 등록
    # url_prefix : url접두사. 해당 블루프린트를 이용할 때 기본적으로 붙을 url을 적음
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    # auth에서 블루프린트 인스턴스 가져오기 및 플라스크 앱에 등록
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    # mypage에서 블루프린트 인스턴스 가져오기 및 플라스크 앱에 등록
    from .mypage import mypage
    app.register_blueprint(mypage, url_prefix='/')

    # DB에 사용할 모델 불러오기
    from .models import User, Note

    # flask-login 적용
    
    # 각 라우터 위에 @login_required 한 것들은 로그인이 필요한 곳이라 정의
    # 다음 코드로 로그인 뷰를 지정했기 때문에 /sign_in으로 이동함
    login_manager = LoginManager()
    # login_manager.login_view = 'auth.sign_in'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(email):
        user = db.users.find_one({'email': email})
        if not user:
            return None
        return User(user['email'], user['nickname'], user['password'])


    return app