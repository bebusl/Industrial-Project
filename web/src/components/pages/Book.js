import { useParams } from "react-router";
import { useEffect, useState } from "react";
import axios from "axios";
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

    useEffect(() => {
        async function get_bookInfo() {
            const data = await axios.get(`http://localhost:5000/book/${bookId}`);
            console.log(data.data.data);
            setInfo({ ...data.data.data });
            setLoading(false);
        }
        get_bookInfo();
    }, []);

    return (
        <>
            {!isLoading && (
                <>
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
                        <button
                            onClick={(e) => {
                                e.preventDefault();
                            }}
                        >
                            장바구니에 담기
                        </button>
                    </div>
                    <div>
                        {book_info.reviews.length > 0
                            ? book_info.reviews.map((k) => (
                                  <div>
                                      <p style={{ textAlign: "left" }}>{k.review}</p>
                                      {k.hasOwnProperty("analysis") && <p>{Object.keys(k.analysis)[0]}</p>}
                                  </div>
                              ))
                            : "리뷰가 없습니다"}
                    </div>
                </>
            )}
        </>
    );
};

export default Book;
