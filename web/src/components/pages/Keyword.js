import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import { Button as ButtonA } from "@mui/material";
import axios from "axios";
import { grid } from "@mui/system";
import { Repeat } from "@mui/icons-material";

const Keyword = () => {
    const { state } = useLocation();
    const navigate = useNavigate();
    const { keywords, books } = state;
    const [select, setSelect] = useState([]);
    const onClick = (name) => {
        console.log(name);
        setSelect([...select, name]);
    };

    const Button = ({ name, onClick, disabled }) => {
        return (
            <ButtonA
                variant="outlined"
                disabled={disabled}
                onClick={(e) => {
                    e.preventDefault();
                    onClick(name);
                }}
            >
                {name}
            </ButtonA>
        );
    };

    return (
        <>
            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(4,1fr)",
                    rowGap: "10px",
                    columnGap: "10px",
                }}
            >
                {keywords.map((i, idx) => (
                    <Button name={i} onClick={onClick} key={idx} disabled={select.includes(i)} />
                ))}
            </div>
            <button
                onClick={async (e) => {
                    e.preventDefault();
                    // const data = await axios.post("http://localhost:5000/recommendation/keywords", {
                    //     books,
                    //     keywords: select,
                    // });
                    const data = [
                        {
                            _id: "61b32d2516d501c9265e1c43",
                            title: "모질게 토익 Economy RC 1000제 (해설집 별매)",
                            isbn: "8950911841",
                            isbn13: "9788950911843.0",
                            itemId: "936500",
                            contents:
                                "해설집이 책의 구성과 특징TOEIC R/C 잘하는 방법Actual Test 01회 정답 및 해설Part 5,6 다시 풀어보기 01회Actual Test 02회 정답 및 해설Part 5,6 다시 풀어보기 02회……………………………..Actual Test 09회 정답 및 해설Part 5,6 다시 풀어보기 09회Actual Test 10회 정답 및 해설Part 5,6 다시 풀어보기 10회정답표문제집이 책을 펴내며더보기해설집이 책의 구성과 특징TOEIC R/C 잘하는 방법Actual Test 01회 정답 및 해설Part 5,6 다시 풀어보기 01회Actual Test 02회 정답 및 해설Part 5,6 다시 풀어보기 02회……………………………..Actual Test 09회 정답 및 해설Part 5,6 다시 풀어보기 09회Actual Test 10회 정답 및 해설Part 5,6 다시 풀어보기 10회정답표문제집이 책을 펴내며Actual Test 1~10회정답표지문 및 문제 해석접기",
                            index: 112754,
                            cover: "https://image.aladin.co.kr/product/93/65/cover500/8950911841_1.jpg",
                            author: "Lori",
                            price: "10000",
                        },
                        {
                            _id: "61b32d2516d501c9265e1b5e",
                            title: "[세트] 해커스 토익 실전 1000제 1 RC 리딩 (문제집 + 해설집) - 전2권",
                            isbn: "K782533662",
                            itemId: "152199281",
                            contents:
                                "해커스 토익 실전 1000제 1 RC 리딩 문제집해커스 토익 실전 1000제 1 RC 리딩 해설집",
                            index: 112525,
                            cover: "https://image.aladin.co.kr/product/15219/92/cover500/k782533662_3.jpg",
                            author: "해커스어학연구소",
                            price: "29800",
                        },
                        {
                            _id: "61b32d2516d501c9265e1cc2",
                            title: "토익이 가벼워지는 토마토 BASIC L/C - 테이프 4개 (교재 별매)",
                            isbn: "8959970360",
                            isbn13: "9788959970360.0",
                            itemId: "607314",
                            index: 112881,
                            cover: "https://image.aladin.co.kr/product/60/73/cover500/8959970360_1.jpg",
                            author: "김묘희",
                            price: "8000",
                        },
                        {
                            _id: "61b32d2516d501c9265e1e12",
                            title: "[세트] 해커스 토익 실전 1000제 2 (LC/RC) (문제집 + 해설집)",
                            isbn: "K952534111",
                            itemId: "176239551",
                            index: 113217,
                            cover: "https://image.aladin.co.kr/product/17623/95/cover500/k952534111_1.jpg",
                            author: "해커스어학연구소",
                            price: "57600",
                        },
                        {
                            _id: "61b32d2516d501c9265e1e1e",
                            title: "[세트] 영단기 토익 실전 1000제 1 RC + LC 문제집 + 해설집 - 전2권",
                            isbn: "K772733793",
                            itemId: "274721128",
                            intro: "'영단기 토익 실전 1000제 1 RC 문제집 + 해설집', '영단기 토익 실전 1000제 1 LC 문제집 + 해설집'으로 구성된 세트 상품이다.",
                            contents:
                                "영단기 토익 실전 1000제 1 RC 문제집 + 해설집영단기 토익 실전 1000제 1 LC 문제집 + 해설집",
                            index: 113229,
                            cover: "https://image.aladin.co.kr/product/27472/11/cover500/k772733793_1.jpg",
                            author: "영단기 연구소",
                            price: "17800",
                        },
                        {
                            _id: "61b32d2516d501c9265e23fe",
                            title: "PAGODA 토익 Basic RC (본서 + 해설서)",
                            isbn: "8962813408",
                            isbn13: "9788962813401.0",
                            itemId: "11984902",
                            index: 114733,
                            cover: "https://image.aladin.co.kr/product/1198/49/cover500/8962813408_1.jpg",
                            author: "파고다교육그룹 언어교육연구소",
                            price: "15000",
                        },
                        {
                            _id: "61b32d2516d501c9265e27b3",
                            title: "김대균의 토익기출 1000제 - 전2권",
                            isbn: "8917173357",
                            isbn13: "9788917173352.0",
                            itemId: "483841",
                            index: 115682,
                            cover: "https://image.aladin.co.kr/product/48/38/cover500/8917173357_1.gif",
                            author: "김대균",
                            price: "35000",
                        },
                        {
                            _id: "61b32d2616d501c9265e2ddd",
                            title: "[세트] 영단기 토익 솔루션 LC + RC - 전2권",
                            isbn: "K962636791",
                            itemId: "214090347",
                            intro: "'영단기 토익 솔루션 LC',  '영단기 토익 솔루션 RC'로 구성된 세트 상품이다.",
                            contents: "영단기 토익 솔루션 LC영단기 토익 솔루션 RC",
                            index: 117260,
                            cover: "https://image.aladin.co.kr/product/21409/3/cover500/k962636791_1.jpg",
                            author: "영단기 연구소",
                            price: "17800",
                        },
                        {
                            _id: "61b32d2616d501c9265e2ff8",
                            title: "[세트] 해커스 토익 실전 1000제 1 Reading + Listening 문제집 (해설집 별매) - 전2권",
                            isbn: "K952532817",
                            itemId: "135436153",
                            intro: "해커스 토익 실전 1000제 1 Reading 문제집과 해커스 신토익 실전 1000제 1 Listening 문제집으로 구성된 세트다.",
                            contents:
                                "해커스 토익 실전 1000제 1 Reading 문제집 (해설집 별매)해커스 신토익 실전 1000제 1 Listening 문제집 (해설집 별매)",
                            index: 117799,
                            cover: "https://image.aladin.co.kr/product/13543/61/cover500/k952532817_1.jpg",
                            author: "해커스어학연구소",
                            price: "23800",
                        },
                        {
                            _id: "61b32d2616d501c9265e30ab",
                            title: "토익이 가벼워지는 토마토 BASIC L/C - 테이프 4개 (교재 별매)",
                            isbn: "8959972665",
                            isbn13: "9788959972661.0",
                            itemId: "2720866",
                            index: 117978,
                            cover: "https://image.aladin.co.kr/product/272/8/cover500/8959972665_1.jpg",
                            author: "이성룡",
                            price: "10000",
                        },
                    ];
                    //navigate("/ranking", { state: data.data.data });
                    navigate("/ranking", { state: data });
                    console.log(data);
                }}
            >
                추천받기
            </button>
            <button
                onClick={(e) => {
                    e.preventDefault();
                    setSelect([]);
                }}
            >
                초기화하기
            </button>

            {select.map((i, idx) => {
                return (
                    <p>
                        {idx + 1}순위 : {i}
                    </p>
                );
            })}
        </>
    );
};

export default Keyword;
