# Blueprint를 이용하면 플라스크 app의 모든 url을 한 곳에서 관리하지 않아도 됨
# 여러곳에 뿌려진 url의 정의를 수집하여 한 곳을 모아줌

from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note, Wishlist, User
from . import db
from bson.objectid import ObjectId
from bson import json_util
# 뷰를 정의하여 보여질 페이지와 경로를 정의
# '클라이언트 요청 > 서버의 응답'을 과정을 세부적이게 구현할 필요가 없음
views = Blueprint('views', __name__)


# @views.route('/')
# @login_required
# def home():
#     all_wishlists = list(db.wishlist.find({}))
#     return render_template('home.html'), json_util.dumps({'result': all_wishlists})


@views.route('/detail')
@login_required
def detail():
    return render_template('detail.html')


@views.route('/', methods=['GET', 'POST'])
def wishlist():
    if request.method == "POST":
        # wishlist_give찾음 wishlist_receive라는 변수에 넣고 print하고 msg 전달하고 -> index.html
        inputGroupSelect01 = request.form['inputGroupSelect01_give']
        mypostit = request.form['mypostit_give']
        myoneline = request.form['myoneline_give']
        floatingTextarea = request.form['floatingTextarea_give']
        myurl = request.form['myurl_give']
        mydate = request.form['mydate_give']

        # 유효성 검사
        if len(mypostit) < 1 or len(myoneline) < 1:
            flash("제목 또는 한줄다짐 내용이 없습니다. 1자 이상 적어주세요.", category="error")
        elif len(floatingTextarea) > 300:
            flash("내용이 너무 깁니다. 300자 이내로 작성해주세요.", category="error")
        else:
            new_list = Wishlist(inputGroupSelect01=inputGroupSelect01,
                                mypostit=mypostit,
                                myoneline=myoneline,
                                floatingTextarea=floatingTextarea,
                                myurl=myurl,
                                mydate=mydate,
                                email=current_user.email)
            new_list.save()
            flash("메모 생성 완료", category="success")
            return redirect(url_for('views.wishlist'))

    return render_template('home.html')


@views.route("/wishlist", methods=["GET"])
def wishlist_get():
    all_wishlists = list(db.wishlist.find({}))
    return json_util.dumps({'result': all_wishlists})


######################################################
@views.route('/memo', methods=['GET', 'POST'])
@login_required
def memo():
    # POST : 메모 생성
    if request.method == "POST":
        title = request.form['note-title']
        content = request.form['note-content']

        # 유효성 검사
        if len(title) < 1 or len(content) < 1:
            flash("제목 또는 내용이 없습니다.", category="error")
        elif len(title) > 50:
            flash("제목이 너무 깁니다. 50자 이내", category="error")
        elif len(content) > 2000:
            flash("내용이 너무 깁니다. 2000자 이내", category="error")
        else:
            # note 인스턴스 생성 -> DB에 저장
            new_note = Note(title=title,
                            content=content,
                            email=current_user.email)
            new_note.save()
            flash("메모 생성 완료", category="success")
            return redirect(url_for('views.memo'))

    notes = list(db.notes.find({'email': current_user.email}))
    return render_template('memo.html', notes=notes)


@views.route('/memo/delete-note', methods=['POST'])
def delete_note():
    # POST : 메모 삭제
    if request.method == "POST":
        note = request.get_json()
        note_id = note.get('noteId')
        # 노트를 삭제합니다.
        db.notes.delete_one({"_id": ObjectId(note_id)})
        return jsonify({})
        # select_note = Note.query.get(note_id)
        # if select_note:
        #     if select_note.email == current_user.email :
        #         db.note.delete_one({'_id':note_id})
        # return jsonify({})

    # return render_template('memo.html')
