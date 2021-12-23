import { useParams } from "react-router";
import { useEffect, useState } from "react";
import { Button } from "@mui/material";
import axios from "axios";
import "d3-transition";
import ReactWordCloud from "react-wordcloud";

import "tippy.js/dist/tippy.css";
import "tippy.js/animations/scale.css";
/*
{
    "_id": "61b32d2516d501c9265e1c43",
    "title": "모질게 토익 Economy RC 1000제 (해설집 별매)",
    "isbn": "8950911841",
    "isbn13": "9788950911843.0",
    "itemId": "936500",
    "contents": "해설집이 책의 구성과 특징TOEIC R/C 잘하는 방법Actual Test 01회 정답 및 해설Part 5,6 다시 풀어보기 01회Actual Test 02회 정답 및 해설Part 5,6 다시 풀어보기 02회……………………………..Actual Test 09회 정답 및 해설Part 5,6 다시 풀어보기 09회Actual Test 10회 정답 및 해설Part 5,6 다시 풀어보기 10회정답표문제집이 책을 펴내며더보기해설집이 책의 구성과 특징TOEIC R/C 잘하는 방법Actual Test 01회 정답 및 해설Part 5,6 다시 풀어보기 01회Actual Test 02회 정답 및 해설Part 5,6 다시 풀어보기 02회……………………………..Actual Test 09회 정답 및 해설Part 5,6 다시 풀어보기 09회Actual Test 10회 정답 및 해설Part 5,6 다시 풀어보기 10회정답표문제집이 책을 펴내며Actual Test 1~10회정답표지문 및 문제 해석접기",
    "index": 112754,
    "cover": "https://image.aladin.co.kr/product/93/65/cover500/8950911841_1.jpg",
    "author": "Lori",
    "price": "10000"
}

[
    {
        "review": "차별화된 문제집 저렴하면서 속이 꽉 찬 문제집"
    },
    {
        "review": "토익은 역시 뭐니뭐니해도 문제만 풀면 되기에 이 책 강추",
        "analysis": {
            "은": {
                "POS": 1,
                "NEG": 0
            }
        }
    },
    {
        "review": "적절한 난이도로 실전 연습에 있어서 유용합니다",
        "analysis": {
            "전": {
                "POS": 1,
                "NEG": 0
            }
        }
    },
    {
        "review": "저렴한 가격으로 양질의 1000문제를 풀수 있는 좋은기회",
        "analysis": {
            "으로": {
                "POS": 1,
                "NEG": 0
            }
        }
    },

]

*/
const Book = () => {
    const { bookId } = useParams();
    const [book_info, setInfo] = useState({});
    const [isLoading, setLoading] = useState(true);
    const [word, setWord] = useState({});
    useEffect(() => {
        async function get_bookInfo() {
            let data = await axios.get(`http://localhost:5000/book/${bookId}`);
            let word = {};
            let word_ = [];
            data = data.data.data;
            data.reviews.forEach((i) => {
                for (const y in i.analysis) {
                    if (!word.hasOwnProperty(y)) {
                        word[y] = { POS: 0, NEG: 0 };
                    }
                    word[y]["POS"] += i.analysis[y]["POS"];
                    word[y]["NEG"] += i.analysis[y]["NEG"];
                }
            });

            for (const t in word) {
                word_.push({
                    text: t,
                    value: word[t]["POS"] + word[t]["NEG"],
                    POS: word[t]["POS"],
                    NEG: word[t]["NEG"],
                });
            }
            setWord([...word_]);
            setInfo({ ...data });
            setLoading(false);
            console.log(word_);
        }
        get_bookInfo();
    }, []);

    const callbacks = {
        getWordColor: (word) => (word["POS"] >= word["NEG"] ? "#1976d2" : "red"),
        getWordTooltip: (word) => `${word.text} 긍정:${word.POS} 부정:${word.NEG}`,
    };
    const options = {
        deterministic: false,
        fontFamily: "impact",
        fontSizes: [20, 80],
        fontStyle: "normal",
        fontWeight: "normal",
        padding: 1,
        rotationAngles: [0, 30],
    };

    function printKeyword(keyword) {
        let pos_result = [];
        let neg_result = [];
        for (const key in keyword) {
            const POS = keyword[key]["POS"];
            const NEG = keyword[key]["NEG"];

            if (POS >= NEG) {
                pos_result.push(key);
            } else {
                neg_result.push(key);
            }
        }
        return (
            <div className="keywords" style={{ display: "inline-block", textAlign: "left", fontSize: "0.7rem" }}>
                {pos_result.map((pos) => (
                    <span className="pos" style={{ fontWeight: "bold" }}>
                        {`${pos}  `}
                    </span>
                ))}
                {neg_result.map((neg) => (
                    <span className="neg" style={{ fontWeight: "bold" }}>
                        {neg}
                    </span>
                ))}
            </div>
        );
    }

    return (
        <>
            {!isLoading && (
                <div style={{ width: "80vw", margin: "auto" }}>
                    <div
                        style={{
                            minHeight: "0px",
                            display: "grid",
                            gridTemplateColumns: "1fr 3fr",
                            gridTemplateRows: "repeat(5,2rem)",
                            margin: "2rem 0",
                            padding: "1rem 0",
                            borderBottom: "1px solid #ececec",
                            textAlign: "left",
                            cursor: "pointer",
                        }}
                        onClick={(e) => {
                            e.preventDefault();
                        }}
                    >
                        <img
                            style={{ gridColumn: "1", gridRow: "1 / span 5", justifySelf: "center" }}
                            alt="cover"
                            src={book_info.book_info.cover}
                            width="150px"
                        />
                        <h5 style={{ margin: 0 }}>{book_info.book_info.title}</h5>
                        <p style={{ margin: 0 }}>{book_info.book_info.price}원 |</p>
                        <p style={{ margin: 0 }}>지은이 {book_info.book_info.author}</p>
                        <p style={{ margin: 0 }}>isbn : {book_info.book_info.isbn}</p>
                        <Button
                            variant="outlined"
                            onClick={(e) => {
                                e.preventDefault();
                                e.stopPropagation();
                                axios
                                    .get(`http://localhost:5000/wishlist/${book_info._id}`, { withCredentials: true })
                                    .then((res) => console.log(res))
                                    .catch((e) => {
                                        if (e.response.status === 501) {
                                            window.alert("로그인이 필요합니다.");
                                        }
                                    });
                            }}
                        >
                            장바구니에 담기
                        </Button>
                    </div>
                    <div style={{ height: 400, width: 600, textAlign: "left" }}>
                        {word.length === 0 ? undefined : (
                            <>
                                <h3>워드클라우드</h3>
                                <ReactWordCloud options={options} words={word} callbacks={callbacks} />
                            </>
                        )}
                    </div>
                    <div style={{ textAlign: "left" }}>
                        <h3>책 정보</h3>
                        <p>{book_info.book_info.hasOwnProperty("intro") ? book_info.book_info.intro : ""}</p>
                    </div>
                    <div>
                        <h3 style={{ textAlign: "left" }}>리뷰</h3>
                        {book_info.reviews.length > 0
                            ? book_info.reviews.map((k, idx) => (
                                  <>
                                      <div key={`rv-${idx}`} style={{ textAlign: "left" }}>
                                          <p style={{ textAlign: "left", fontSize: "0.8rem", display: "inline-block" }}>
                                              {k.review}
                                          </p>
                                          {printKeyword(k.analysis)}
                                      </div>
                                      <hr style={{ border: "1px solid #ececec" }} />
                                  </>
                              ))
                            : "리뷰가 없습니다"}
                    </div>
                </div>
            )}
        </>
    );
};

export default Book;
