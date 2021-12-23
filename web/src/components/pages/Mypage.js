import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

const Mypage = () => {
    const navigate = useNavigate();
    const [state, setState] = useState([]);
    function fetch() {
        axios
            .get("http://localhost:5000/user/", { withCredentials: true })
            .then((res) => setState(res.data.data))
            .catch((e) => console.log(e));
    }
    useEffect(() => {
        function fetch() {
            axios
                .get("http://localhost:5000/user/", { withCredentials: true })
                .then((res) => setState(res.data.data))
                .catch((e) => console.log(e));
        }
        fetch();
    }, []);

    return (
        <>
            {state.length == 0 ? (
                <h4>장바구니 목록이 없습니다.</h4>
            ) : (
                <div style={{ width: "80vw", margin: "auto", textAlign: "left" }}>
                    <h2>장바구니</h2>
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
                                        .delete(`http://localhost:5000/wishlist/${i["_id"]}`, { withCredentials: true })
                                        .then((res) => fetch())
                                        .catch((e) => console.log(e));
                                }}
                            >
                                장바구니에서 빼기
                            </Button>
                        </div>
                    ))}
                </div>
            )}
            <Button
                variant="contained"
                onClick={(e) => {
                    e.preventDefault();
                    axios.get("http://localhost:5000/auth/logout", { withCredentials: true }).then((res) => {
                        console.log(res);
                        if (res.status === 200) {
                            navigate("/");
                        }
                    });
                }}
            >
                로그아웃
            </Button>
        </>
    );
};
