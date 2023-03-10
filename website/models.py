from flask_login import UserMixin
from datetime import datetime
from bson.objectid import ObjectId
from . import db
from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient(
    'mongodb+srv://joonyeol:1234@sparta.afgjtfy.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

# forign key 역할을 해주는 objectid
# flask_login의 UserMixin 클래스 상속
# flask_login은 Flask에 대한 사용자 세션 관리를 제공
# 세션에 활성 사용자의 id를 저장하고 쉽게 로그인/로그아웃 할 수 있음
# 로그인 or 로그아웃한 사용자의 보기 제한 등

# User Model 정의


class User(UserMixin):
    def __init__(self, email, nickname, password, image=None):
        self.email = email
        self.nickname = nickname
        self.password = password
        self.image = image

    def save(self):
        user_data = {
            'email': self.email,
            'nickname': self.nickname,
            'password': self.password,
        }
        db.users.insert_one(user_data)

    @classmethod
    def get(cls, email):
        user_data = db.users.find_one({'email': email})
        if user_data:
            return cls(email=user_data['email'],
                       nickname=user_data['nickname'],
                       password=user_data['password'])
        else:
            return None

    def get_id(self):
        return str(self.email)


# Note Model 정의

class Note:
    def __init__(self, title, content, email):
        self.title = title
        self.content = content
        self.datetime = datetime.now()
        self.email = email

    def save(self):
        note_data = {
            'title': self.title,
            'content': self.content,
            'datetime': self.datetime,
            'email': self.email,

        }
        db.notes.insert_one(note_data)

    @classmethod
    def get(cls, email):
        note_data = list(db.notes.find({'email': email}))
        return cls(title=note_data['title'],
                   content=note_data['content'],
                   datetime=note_data['datetime'],
                   email=note_data['email'],
                   id=note_data['_id'])

# Wishlist 정의


class Wishlist:
    def __init__(self, inputGroupSelect01, mypostit, myoneline, floatingTextarea, myurl, mydate, email, nickname):
        self.inputGroupSelect01 = inputGroupSelect01
        self.mypostit = mypostit
        self.myoneline = myoneline
        self.floatingTextarea = floatingTextarea
        self.myurl = myurl
        self.mydate = mydate or datetime.now()
        self.email = email
        self.nickname = nickname

    def save(self):
        wishlist_data = {
            'inputGroupSelect01': self.inputGroupSelect01,
            'mypostit': self.mypostit,
            'myoneline': self.myoneline,
            'floatingTextarea': self.floatingTextarea,
            'myurl': self.myurl,
            'mydate': self.mydate,
            'email': self.email,
            'nickname': self.nickname
        }
        db.wishlist.insert_one(wishlist_data)


class Comment:
    def __init__(self, email, nickname, comment, post_id):
        self.date = datetime.now()
        self.email = email
        self.nickname = nickname
        self.comment = comment
        self.post_id = post_id

    def save(self):
        comment_data = {
            'email': self.email,
            'nickname': self.nickname,
            'comment': self.comment,
            'date': self.date,
            'post_id': self.post_id
        }
        db.comments.insert_one(comment_data)
