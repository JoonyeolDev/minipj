from flask_login import UserMixin
from datetime import datetime
from bson.objectid import ObjectId
from . import db
from pymongo import MongoClient
client = MongoClient(
    'mongodb+srv://joonyeol:1234@sparta.afgjtfy.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# forign key 역할을 해주는 objectid
# flask_login의 UserMixin 클래스 상속
# flask_login은 Flask에 대한 사용자 세션 관리를 제공
# 세션에 활성 사용자의 id를 저장하고 쉽게 로그인/로그아웃 할 수 있음
# 로그인 or 로그아웃한 사용자의 보기 제한 등

# User Model 정의


class User(UserMixin):
    def __init__(self, email, nickname, password, image_path=None):
        self.email = email
        self.nickname = nickname
        self.password = password
        self.image_path = image_path

    def save(self):
        user_data = {
            'email': self.email,
            'nickname': self.nickname,
            'password': self.password,
        }
        result = db.users.insert_one(user_data)
        self._id = result.inserted_id

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
            'email': self.email
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


# Note Model 정의
