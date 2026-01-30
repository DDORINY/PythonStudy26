from LMS.common.Session import Session
from LMS.service import *

def main():
    run =True
    while run:
        MemberService.load()

        print("""
+--------------------------------------+
|        MBC 아카데미 LMS 프로그램       |
+--------------------------------------+
  [1] 회원가입
  [2] 로그인
  [3] 로그아웃
  [4] 회원관리
  [5] 게시판
  [6] 쇼핑몰
----------------------------------------
  [9] 관리자 페이지
  [0] 프로그램 종료
        """)
        member = Session.login_member
        if member is None:
            print("현재 로그인 상태가 아닙니다.")
        else:
            print(f"{member.name}님 환영합니다.")

        select = input(">>>")

        if select == "1":
            print("""
+--------------------------------------+
|        MBC 아카데미 LMS 회원가입       |
+--------------------------------------+
    """)
            MemberService.signup()
        elif select == "2":
            print("""
+--------------------------------------+
|         MBC 아카데미 LMS 로그인        |
+--------------------------------------+
    """)
            MemberService.login()
        elif select == "3":
            print("""
+--------------------------------------+
|        MBC 아카데미 LMS 로그아웃       |
+--------------------------------------+
            """)
            MemberService.logout()
        elif select == "4":
            print("""
+--------------------------------------+
|        MBC 아카데미 LMS 회원관리       |
+--------------------------------------+
            """)
            MemberService.modify()
        elif select == "5":
            print("""
+--------------------------------------+
|         MBC 아카데미 LMS 게시판        |
+--------------------------------------+
            """)
        elif select == "6":
            print("""
+--------------------------------------+
|         MBC 아카데미 LMS 쇼핑몰        |
+--------------------------------------+
            """)
        elif select == "9":
            MemberService.admin_p()

        elif select == "0":
            print("""
+--------------------------------------+
|      MBC 아카데미 LMS 프로그램 종료     |
+--------------------------------------+
                        """)
            run = False
        else:return


if __name__ == "__main__":
    main()