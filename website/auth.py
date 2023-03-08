# request : 클라이언트 요청에 대한 데이터
# flash : 서버에서 처리, 오류/처리사항을 HTML에 넘겨주는 기능
# info - 단순 알림, error - 오류로 처리불가, warning - 오류가 있으나 넘어감 
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

# init.py ㄱㄱ


# 로그인, 로그아웃, 회원가입 페이지의 url을 정의
# route 함수에 추가적인 url을 작성하여 분기를 만들어줌

# 페이지 접속 > GET
# 회원가입 신청 > POST
@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form['email']
        password1 = request.form['password1']

        # 데이터베이스에서 가입된 유저 찾기 및 비밀번호 대조하기
        user = User.get(email=email)
        #user = db.users.find_one({'email': email})
        if user:
            if check_password_hash(user.password, password1):
                flash('로그인 완료', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else: 
                flash('비밀번호가 다릅니다.', category='error')
        else:
            flash('해당 이메일 정보가 없습니다.', category='error')

    return render_template('sign_in.html')


@auth.route('/logout')
# 로그아웃은 로그인이여야만 가능하도록 view호출 전에 로그인인지 확인요청
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.sign_in'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # 데이터 확인
    # data = request.form
    # print(data)
    # GET으로 요청할 때는 안나오고 POST로 요청해야 나옴

    if request.method == 'POST':
        # form - input의 name 속성을 기준으로 가져오기
        email = request.form['email']
        nickname = request.form['nickname']
        password1 = request.form['password1']
        password2 = request.form['password2']

        # 유효성 검사
        user = db.users.find_one({'email': email})
        if user:
            flash("이미 가입된 이메일입니다.", category='error')
        if len(email) < 5 :
            flash("이메일은 5자 이상으로 적어주세요.", category="error")
        elif len(nickname) < 2:
            flash("닉네임은 2자 이상으로 적어주세요.", category="error")
        elif len(password1) < 7:
            flash("비밀번호가 너무 짧습니다.", category="error")
        elif password1 != password2 :
            flash("비밀번호와 비밀번호 재입력이 서로 다릅니다.", category="error")
        else:
            # if문을 모두 통과하면, Save User -> DB
            new_user = User(email=email, nickname=nickname, password=generate_password_hash(password1, method='sha256'))
            new_user.save() 

            # auto-login
            login_user(new_user, remember=True)
            flash("회원가입 완료.", category="success")  
            return redirect(url_for('views.home'))


    return render_template('sign_up.html')

# main.py ㄱㄱ