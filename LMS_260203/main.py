from common import *
from service import *

def main():
    MemberService.load()
    run =True
    while run:
        print("""
        ------------------------
         MBC 아카데미 LMS 프로그램 
        ------------------------
        [1] 로그인
        [2] 회원가입
        [3] 내정보보기
        ------------------------
        [0] 프로그램 종료
        """)
        select =input(">>>")
        if select =="1":MemberService.login()
        elif select =="2":MemberService.signup()
        elif select =="3":MemberService.modify()
        elif select =="0":run = False

if __name__ == "__main__":
    main()