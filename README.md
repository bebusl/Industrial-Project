# 키워드 기반 도서 추천 서비스
산학프로젝트 윤이버스조


## 의존성 및 설치 방법
* 용량이 큰 파일은 git에 올리지 않았음.
* 모델( checkpoint-1200 ) 파일은 다운로드 받아서 server/celery/model/ 위치에 넣어주어야 함
* tfidf 매트릭스 파일도 다운로드받아 sever/celery/model폴더에 넣어주어야 함.
* .env파일을 server/env파일에 생성해주어야 함.(key 내용 문의 :  bebus1998@naver.com)


[정환추가]
[정은추가]

--------------------------------
### api server
        "bcryptjs": "^2.4.3",
        "body-parser": "^1.19.0",
        "cookie-parser": "^1.4.5",
        "cors": "^2.8.5",
        "dotenv": "^10.0.0",
        "express": "^4.17.1",
        "jsonwebtoken": "^8.5.1",
        "mongoose": "^6.0.11",
        "nodemon": "^2.0.13",
        "swagger-autogen": "^2.13.0",
        "swagger-ui-express": "^4.1.6"
'npm i'
'pip install -r requirements.txt'

## 실행방법(development)
### api 서버 오픈
```
cd server
npm i
npm run dev
```
[정은 추가]
[정환 추가]


## 라이센스
