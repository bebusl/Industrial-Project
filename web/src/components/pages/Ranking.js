import { useLocation, useNavigate } from "react-router";
import axios from "axios";
import { Button } from "@mui/material";
const Ranking = () => {
    const { state } = useLocation();
    const navigate = useNavigate();

    console.log(state);
    /*data 형태
    {
    "_id": "61b32d2516d501c9265e1c43",
    "title": "모질게 토익 Economy RC 1000제 (해설집 별매)",
    "isbn": "8950911841",
    "isbn13": "9788950911843.0",
    "itemId": "936500",
    "contents": "해설집이 책의 구성과 특징TOEIC R/C 잘하는 방법Actual Test 01회 정답 및 해설Part 5,6 다시 풀어보기 01회Actual Test 02회 정답 및 해설Part 5,6 다시 풀어보기 02회……………………………..Actual Test 09회 정답 및 해설Part 5,6 다시 풀어보기 09회Actual Test 10회 정답 및 해설Part 5,6 다시 풀어보기 10회정답표문제집이 책을 펴내며더보기해설집이 책의 구성과 특징TOEIC R/C 잘하는 방법Actual Test 01회 정답 및 해설Part 5,6 다시 풀어보기 01회Actual Test 02회 정답 및 해설Part 5,6 다시 풀어보기 02회……………………………..Actual Test 09회 정답 및 해설Part 5,6 다시 풀어보기 09회Actual Test 10회 정답 및 해설Part 5,6 다시 풀어보기 10회정답표문제집이 책을 펴내며Actual Test 1~10회정답표지문 및 문제 해석접기",
    "intro":"인트로테스트인트로테스트"
    "index": 112754,
    "cover": "https://image.aladin.co.kr/product/93/65/cover500/8950911841_1.jpg",
    "author": "Lori",
    "price": "10000"
}
    
    */
    return (
        <div style={{ width: "80vw", margin: "auto", textAlign: "left" }}>
            <h2>추천 리스트</h2>
            {state.map((i, idx) => (
                <div
                    key={idx}
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
                        navigate(`/book/${i["_id"]}`);
                    }}
                >
                    <img
                        style={{ gridColumn: "1", gridRow: "1 / span 5", justifySelf: "center" }}
                        alt="cover"
                        src={i.cover}
                        width="150px"
                    />
                    <h5 style={{ margin: 0 }}>{i.title}</h5>
                    <p style={{ margin: 0 }}>{i.price}원 |</p>
                    <p style={{ margin: 0 }}>지은이 {i.author}</p>
                    <p style={{ margin: 0 }}>isbn : {i.isbn}</p>
                    <Button
                        variant="outlined"
                        onClick={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            axios
                                .get(`http://localhost:5000/wishlist/${i["_id"]}`, { withCredentials: true })
                                .then((res) => console.log(res))
                                .catch((e) => console.log(e));
                        }}
                    >
                        장바구니에 담기
                    </Button>
                </div>
            ))}
        </div>
    );
};

export default Ranking;
