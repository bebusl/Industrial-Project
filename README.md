# 키워드 기반 도서 추천 서비스
### contributor
|이진희|윤정환|이정은|
|------|---|---|
| [bebusl](https://github.com/bebusl)              |      [dungbik](https://github.com/dungbik)         |   [leejeongeun0](https://github.com/leejeongeun0)      |
| 🌴                                               | 🔥                                               | 📖                                               |



#### 서비스 설명
해당 서비스, 연관 키워드 기반 도서 추천 서비스는 사용자의 기분과 취향 등을 나타내는 키워드에 밀접하게 연관된 도서를 추천해주는 안드로이드 기반 앱이다.

1. 사용자에게 입력받은 키워드를 이용하여 도서를 추천한다.
사용자에게 원하는 장르나 취향의 키워드를 입력하게한다. 입력된 키워드는 유사한 키워드를 추출하고 본 키워드와 데이터 베이스에 저장해놓은 정보를 비교하여 연관성이 높은 도서찾는다. 도서의 리뷰에 등록된 키워들를 추출하고, 사용자에게 선호도를 조사하여 최종적인 도서 추천 순위를 사용자에게 제공한다.

2. 사용자는 키워드들의 선호도를 체크할 수 있다.
입력한 키워드의 도서를 선정하였을 때, 사용자의 의도와 맞지 않은 도서가 선별될 수 있으므로 사용자가 도서의 리뷰에서 추출된 키워드의 선호도를 직접 선택하여 추천 서비스의 정확도와 만족감을 높인다.
-----
## 샘플
![20211211_233338](https://user-images.githubusercontent.com/49610681/145680429-1a715747-111f-4d9b-9ebd-6a0ac5ef21e4.gif)


## 의존성 및 설치 방법
* 용량이 큰 파일은 git에 올리지 않았음.
* 모델( checkpoint-1200 ) 파일은 다운로드 받아서 server/celery/model/ 위치에 넣어주어야 함
* tfidf 매트릭스 파일도 다운로드받아 sever/celery/model폴더에 넣어주어야 함.
* .env파일을 server/env파일에 생성해주어야 함.(key 내용 문의 :  bebus1998@naver.com)


### api server
*  의존성
      ```  "bcryptjs": "^2.4.3",
        "body-parser": "^1.19.0",
        "cookie-parser": "^1.4.5",
        "cors": "^2.8.5",
        "dotenv": "^10.0.0",
        "express": "^4.17.1",
        "jsonwebtoken": "^8.5.1",
        "mongoose": "^6.0.11",
        "nodemon": "^2.0.13",
        "swagger-autogen": "^2.13.0",
        "swagger-ui-express": "^4.1.6"```
* 설치방법
     ```
        cd server
        npm i
        cd server/celery
        pip install -r requirements.txt
    ```

### flutter-app
[flutter install](https://docs.flutter.dev/get-started/install)
<br />

## 실행방법(development)
### api 서버 오픈
```
cd server
npm i
npm run dev
```

### flutter app 빌드
```
cd flutter-app
flutter build apk (android)
flutter build ios (ios)
```



----
## License
```
The MIT License (MIT)

Copyright (c) 2021 yoonleeverse

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

```
