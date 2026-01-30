from LMS.domain import *
from LMS.common import *

class MemberService:

    @classmethod
    def load(cls):
        # [1] DB 연결 객체 생성 (MySQL 서버 접속)
        conn = Session.get_connection()
        try:
            # [2] DictCursor 생성
            # → SELECT 결과를 dict 형태로 받기 위함
            with conn.cursor() as cursor:
                # [3] members 테이블의 전체 회원 수를 조회
                # COUNT(*) 결과를 cnt 라는 별칭(alias)으로 지정
                cursor.execute("SELECT COUNT(*) AS cnt FROM members")
                # [4] 조회 결과 중 첫 번째 행을 가져옴
                # 반환 예시: {'cnt': 10}
                row = cursor.fetchone()
                # [5] 딕셔너리에서 cnt 값(회원 수)만 추출
                count = row['cnt']
                # (선택) 조회된 회원 수 출력 또는 클래스 변수에 저장
                # print(f"전체 회원 수: {count}")
                # cls.total_count = count

                # execute()  →  DB에서 결과 생성
                # fetchone() →  결과 중 1행 꺼내오기
        finally:
            # [6] DB 연결 종료 (예외 발생 여부와 관계없이 실행)
            conn.close()

    @classmethod
    def login(cls):
        print("로그인페이지로 진입하였습니다.")
        uid = input("아이디 : ")
        pw = input("비밀번호 : ")

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql="SELECT * FROM members WHERE uid = %s and password =%s"
                cursor.execute(sql,(uid,pw))
                row = cursor.fetchone()

                if row :
                    member =Member.from_db(row)
                    if not member.active:
                        print("비활성화 계정입니다.\n관리자에게 문의해주세요.")
                        return
                    Session.login(member)
                    print(f"{member.name}님 로그인되었습니다.\n환영합니다.")
        finally:conn.close()

    @classmethod
    def logout(cls):
        if not Session.is_login :
            print("로그인 상태가 아닙니다.")
            return

        Session.logout()
        print("로그아웃되었습니다.")

    @classmethod
    def signup(cls):
        print("회원가입 페이지로 진입하였습니다.")
        uid = input("아이디 : ")

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql="SELECT id FROM members WHERE uid = %s"
                cursor.execute(sql,(uid,))
                row = cursor.fetchone()

                if row:
                    print("이미 존재하는 아이디입니다.")
                    return
                pw = input("비밀번호 : ")
                name = input("이름 : ")

                insert_sql="INSERT INTO members (uid,password,name) VALUES (%s,%s,%s)"
                cursor.execute(insert_sql,(uid,pw,name))
                conn.commit()
                print("회원가입이 완료되었습니다.")
        finally:conn.close()


    @classmethod
    def modify(cls):
        if not Session.is_login :
            print("로그인 후 이용 가능합니다.")
            return
        member =Session.login_member
        print(f"""
이름 : {member.name}| 아이디 : {member.uid}|{member.pw}| 권한 : {member.role}""")

        print("""
+--------------------------------------+
[내 정보 수정] 
[1] 이름변경        [2] 비밀번호변경 
[3] 탈퇴 및 비활성화 [0] 취소""")
        sel =input(">>>")
        if sel == "1":
            new_name = input("새 이름 : ")
        elif sel == "2":
            new_pw = input("새 비밀번호 : ")
        elif sel == "3":
            cls.delete()
        else : return
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql="UPDATE members SET name = %s,password = %s WHERE id = %s"
                cursor.execute(sql,(new_name,new_pw,member.id))
                conn.commit()

                member.name = new_name
                member.pw = member.pw
                print("정보가 수정되었습니다.")
        finally:conn.close()

    @classmethod
    def delete(cls):
        if not Session.is_login :return
        member =Session.login_member
        print("""
+--------------------------------------+
[회원탈퇴] 
[1] 회원탈퇴   [2] 비활성화   [0]취소
        """)
        sel =input(">>>")

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                if sel == "1":
                    sql="DELETE FROM members WHERE id = %s"
                    cursor.execute(sql,member.id)
                    print("회원탈퇴가 완료되었습니다.")
                elif sel == "2":
                    sql = "UPDATE members SET active = FALSE WHERE id = %s"
                    cursor.execute(sql,member.id)
                    print("계정이 비활성화되었습니다.")

                conn.commit()
                Session.logout()
        finally:conn.close()

    @classmethod
    def admin_p(cls):
        if not Session.is_login():
            print("관리자 전용페이지입니다.")
            return

        if Session.is_admin():
            print("""
+--------------------------------------+
|        MBC 아카데미 LMS 회원관리       |
+--------------------------------------+
회원관리 관리자 전용 페이지입니다. 
[1] 회원목록조회
[2] 계정차단/복구
[3] 권한설정 
----------------------------------------
[0] 메인메뉴로 돌아가기""")
            sel = input(">>>")
            if sel == "1":cls.list_members()
            elif sel == "2":cls.change_role()
            elif sel == "3":cls.change_active()
            else : return
    @classmethod
    def list_members(cls):
        print("""
+--------------------------------------+
|        MBC 아카데미 LMS 회원목록       |
+--------------------------------------+""")
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql="SELECT * FROM members ORDER BY id DESC"
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    m=Member.from_db(row)
                    status = "활성" if m.active else "비활성"
                    print(f"{m.id} | 이름 :{m.name} | 아이디 : {m.uid} | 권한 : {m.role} | 상태 : {status}")
                    print("--------------------------------------------------------------")
        finally:conn.close()

    @classmethod
    def change_role(cls):pass
    @classmethod
    def change_active(cls):pass