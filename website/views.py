# Blueprint를 이용하면 플라스크 app의 모든 url을 한 곳에서 관리하지 않아도 됨
# 여러곳에 뿌려진 url의 정의를 수집하여 한 곳을 모아줌

from flask import Blueprint, render_template
from flask_login import login_required, current_user

# 뷰를 정의하여 보여질 페이지와 경로를 정의
# '클라이언트 요청 > 서버의 응답'을 과정을 세부적이게 구현할 필요가 없음
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html')


# __init__.py 로 ㄱㄱ

