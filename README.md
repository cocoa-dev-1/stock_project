# # 주식 가상투자 프로그램

시스템 게획:
 1. 처음 가상자산은 동일
 2. 정해진 기간을 바탕으로 하는 유저들의 주식 거래
 3. 주식종류는 2~3가지
 4. 각 주식에 대한 자본으로 바탕으로 랭킹 표시
 5. 만약 가능하다면 유저들의 실시간 채팅 (socket 활용)
 6. 클라이언트는 DB에 기록된 정보를 바탕으로 원할때 시스템 접속 가능


서버:
 1. 유저의 ID, 비밀번호 등을 저장
 1.2 유저의 비밀번호는 sha3-256 암호화로 해쉬해서 저장(보안)
 2. 유저의 현재 자산 현황, 유저 거래 로그 기록
 3. 주식 장마감, 열리는 시간 확인
 4. socket 통신을 바탕으로한 실시간 채팅
 5. 실제 유저들의 가상 투자 관리(매수, 매도)
 6. 모든 랭킹, 차트, 채팅, 매수,매도 로그 등등은 **실시간으로 모든 접속 유져 동기화**
 

클라이언트:
 1. 주식 API 가져오기
 2. 주식 API를 바탕으로한 주식 차트
 3. 화윈가입, 로그인 데이터 서버 전송
 4. 가상 자산을 바탕으로한 모의 투자
 5. 실제 유저들과 대결
 6. 매수, 매도 로그 시각화
 
필요 기술:
 [pymysql](https://yurimkoo.github.io/python/2019/09/14/connect-db-with-python.html "pyMySQL")
 [socket](https://docs.python.org/ko/3/library/socket.html "socket 통신")
 [API request](https://gosmcom.tistory.com/130 "request API모듈")
 [tkinter GUI](https://docs.python.org/ko/3/library/tkinter.html "tkinter GUI 모듈")
 [matpoltlib](https://wikidocs.net/92071 "차트 그리기 모듈")
