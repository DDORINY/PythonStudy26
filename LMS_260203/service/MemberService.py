from common import *
from common.Session import Session
from domain import *

class MemberService:
    @classmethod
    def load(cls):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT count(*) as cnt FROM members")
                count = cursor.fetchone()["cnt"]
        finally: conn.close()

    @classmethod
    def login(cls):
        if Session.is_login():
            print("이미 로그인되어있습니다.")
            return

        print("로그인 화면입니다.")
        uid = input("아이디 :")
        pw =input("비밀번호 :")

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM members WHERE uid = %s and password=%s"
                cursor.execute(sql, (uid, pw))
                row = cursor.fetchone()
                if row:
                    member =Member.from_db(row)
                    if not member.active:
                        print("비활성화 계정입니다.")
                        return
                    Session.login(member)
                    print(f"{member.name}님 로그인되었습니다.")
                else :print("아이디 또는 비밀번호가 맞지 않습니다.")
        finally: conn.close()


    @classmethod
    def signup(cls):
        new_uid = input("아이디 : ")
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT id FROM members WHERE uid = %s"
                cursor.execute(sql, (new_uid,))
                row = cursor.fetchone()
                if row:
                    print("중복된 아이디입니다.")
                    return
                new_pw = input("비밀번호 : ")
                new_name = input("이름 : ")

                insert_sql = "INSERT INTO members (uid,password, name) VALUES (%s,%s, %s)"
                cursor.execute(insert_sql, (new_uid, new_pw, new_name))
                conn.commit()
                print("회원가입이 완료되었습니다.")
        except:conn.rollback()
        finally: conn.close()

    @classmethod
    def modify(cls):
        pass