import pymysql

class Session:
    login_member = None

    @staticmethod
    def get_connection():
        return pymysql.connect(
            host="localhost",
            user="mbc",
            password="1234",
            db="lms",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
            #SQL 조회 결과를 튜플(tuple)이 아니라 딕셔너리(dict) 형태로 받게 해주는 설정
        )

    @classmethod
    def login(cls,member):
        cls.login_member = member

    @classmethod
    def logout(cls):
        cls.login_member = None

    @classmethod
    def is_login(cls):
        return cls.login_member is not None

    @classmethod
    def is_admin(cls):
        return cls.is_login() and cls.login_member.role == "admin"

    @classmethod
    def is_manager(cls):
        return cls.is_login() and cls.login_member.role in ("manager","admin")

