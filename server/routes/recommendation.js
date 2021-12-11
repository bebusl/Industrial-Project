const router = require("express").Router();
const User = require("../model/user");
const SearchKeyword = require("../model/searchKeyword");
const { isLogin } = require("./middlewares");
const { get_booklist, get_reviews, get_keywords } = require("../celery/node-tasks");
const Book = require("../model/book");
const Review = require("../model/reviews");

//처음 검색
router.get("/:searchKeyword", async (req, res) => {
    const { searchKeyword } = req.params;
    const books = await get_booklist(searchKeyword);
    let datas = await Book.find({ index: { $in: books } }, { _id: 1, title: 1, itemId: 1 });
    let objectIds = datas.reduce((re, cur) => {
        re.push([cur._id, cur.itemId]);
        return re;
    }, []);
    try {
        arr = [];
        for (let i in objectIds) {
            arr.push(get_reviews(objectIds[i]));
        }
        const result = await Promise.all(arr);

        //arr = [get_keywords(result)];
        let books = objectIds.map((cur) => cur[0]);
        arr = [];
        for (let i in result) {
            arr.push(get_keywords(result[i]));
        }
        const result_ = await Promise.all(arr);

        let keywords = [];
        let reviews = [];
        for (let i in result_) {
            reviews = reviews.concat(result_[i][0]);
            keywords = keywords.concat(result_[i][1]);
        }
        //const result_ = await get_keywords(result);
        Review.insertMany(reviews);

        return res.json({
            success: true,
            keywords: [...new Set(keywords)],
            books: books,
        });
    } catch (e) {
        console.log(e);
        return res.json({
            success: false,
            msg: e,
        });
    }

    // if (req.isLogin) {
    //     const id = req.userEmail;
    //     const user = await User.findOne({ id });
    //     SearchKeyword.updateOne({ _id: user["searchKeyword"] }, { $push: { keywords: search } });
    //     //여기서 이제
    //     // 1. 유사한 책 찾아오기
    //     // 2. 키워드 반환.
    //     // 키워드 반환
    // } //로그인 되어 있을 시 searchKeyword에 추가

    /*Update this.rabbitmq 연결하고 키워드 받아오는 거 추가*/
});

//키워드 선택
router.post("/keywords", async (req, res) => {
    //[1순위,2순위,3순위,4순위,5순위]이렇게 해서 보내주기!
    const { books, keywords } = req.body;

    let datas = await Review.find({ bookId: { $in: books } }, { _id: 0, bookId: 1, analysis: 1 });
    let score = books.reduce((re, cur) => {
        re[cur] = keywords.reduce((re, cur) => {
            re[cur] = { POS: 0, NEG: 0 };
            return re;
        }, {});
        return re;
    }, {});

    datas.forEach((i) => {
        for (const j in i.analysis) {
            if (keywords.includes(j)) {
                score[i.bookId][j]["NEG"] += i.analysis[j]["NEG"];
                score[i.bookId][j]["POS"] += i.analysis[j]["POS"];
            }
        }
    });

    let result = [];

    for (const book in score) {
        point = 0;
        for (let i = 0; i < keywords.length; i++) {
            vect = 0;
            let POS = score[book][keywords[i]]["POS"];
            let NEG = score[book][keywords[i]]["NEG"];
            if (POS == 0 && NEG == 0) {
                vect = 0;
            } else vect = (POS - NEG) / (POS + NEG);
            point = point + vect * (100000 / 10 ** (i + 1));
        }
        let temp = new Object();
        temp[book] = point;
        result.push(temp);
    }

    function compare(a, b) {
        a_score = Object.values(a)[0];
        b_score = Object.values(b)[0];
        if (a_score < b_score) {
            return 1;
        }
        if (a_score > b_score) {
            return -1;
        }
        return 0;
    }
    result.sort(compare);
    const result_ = result.map((i) => {
        return Object.keys(i)[0];
    });

    result = [];
    const msg = await Promise.all(
        result_.map((i) => {
            const t = Book.findById(i);
            return t;
        })
    );

    return res.json({
        success: true,
        data: msg,
    });
});

module.exports = router;
