from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note, Wishlist, User
from . import db
from bson.objectid import ObjectId
from bson import json_util
import os
from werkzeug.utils import secure_filename

mypage = Blueprint('mypage', __name__)

# 나의 정보 페이지
@mypage.route('/mypage', methods=['GET','POST'])
@login_required
def mypage_main():
    return render_template('mypage.html')

# 프로필 이미지 확장자 목록
ALLOWED_EXTENSIONS = ['png','jpg','jpeg','gif']

# 확장자 확인
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 나의 정보 수정 페이지
@mypage.route('/mypage/update', methods=['GET','POST'])
@login_required
def mypage_update():
    # 나의 정보 수정 요청 확인
    if request.method == 'POST':
        # 이미지 파일 정보가 있는 지 확인
        if 'imageFile' in request.files:
            image_file = request.files['imageFile']  # 디버그 모드로 확인

            # 파일이 존재하는지 확인
            if image_file.filename:

                # 허용된 파일인지 확인
                if allowed_file(image_file.filename):
                    # secure_filename : 파일을 시스템에서 안전하게 사용할 수 있는 파일 이름으로 반환
                    # 파일 이름에서 경로 구분자 제거, ASCII 이외의 문자를 제거, 공백을 밑줄(_)로 대체, 파일 이름이 마침표(.)로 시작하지 않도록 조치
                    # 파일 이름으로 시스템 명령어 삽입 공격 등 보안 문제 예방
                    filename = secure_filename(image_file.filename)
                    # rsplit : '.'기준으로 스플릿 후 오른쪽을 가져옴
                    # lower : 알파벳 소문자로 변환
                    filetype = filename.rsplit('.', 1)[1].lower()
                    
                    # user id로 프로필 명 저장
                    image_file.save(f'{image_path}{current_user.email}.{filetype}')

                    # DB user.image_path에 반영
                    user = User.query.get(current_user.email)
                    user.image_path = f'{current_user.email}.{filetype}'
                    db.users.update_one({'email':current_user.email},{'$set':{'age':19}})

                    return redirect(url_for('mypage_views.mypage'))
                else:
                    # 확장자가 허용되지 않음
                    flash('이미지 파일은 png jpg jepg gif 만 지원합니다.', category = "error")
                    return redirect(request.url)
    return render_template('mypage.html')