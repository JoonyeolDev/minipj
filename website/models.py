from . import db
from pymongo import MongoClient
client = MongoClient('mongodb+srv://joonyeol:1234@sparta.afgjtfy.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# forign key 역할을 해주는 objectid
from bson.objectid import ObjectId
from datetime import datetime
# flask_login의 UserMixin 클래스 상속
# flask_login은 Flask에 대한 사용자 세션 관리를 제공
# 세션에 활성 사용자의 id를 저장하고 쉽게 로그인/로그아웃 할 수 있음
# 로그인 or 로그아웃한 사용자의 보기 제한 등
from flask_login import UserMixin

# define User Model
class User(UserMixin):
    def __init__(self, email, nickname, password):
        self.email = email
        self.nickname = nickname
        self.password = password
 
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
    def get_notes(self):
        return [Note.get(note_data) for note_data in db.notes.find({'email': self.email})]



# define Note Model

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
    def get(cls, note_data):
        return cls(title=note_data['title'],
                content=note_data['content'],
                datetime=note_data['datetime'],
                email=note_data['email'])