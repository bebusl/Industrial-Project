import { IconButton, InputBase, Paper } from "@mui/material";
import Search from "@mui/icons-material/Search";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./style.css";
import axios from "axios";

const Main = (props) => {
    const [keyword, setKeyword] = useState("");
    let navigate = useNavigate();
    const onSubmit = async (e) => {
        e.preventDefault();
        //const result = await axios.get(`http://localhost:5000/recommendation/${keyword}`);
        const result = {
            success: true,
            keywords: ["은", "전", "으로", "사람들이", "문제를", "실제", "프", "으로"],
            books: [
                "61b32d2516d501c9265e1b5e",
                "61b32d2516d501c9265e1c43",
                "61b32d2516d501c9265e1cc2",
                "61b32d2516d501c9265e1e12",
                "61b32d2516d501c9265e1e1e",
                "61b32d2516d501c9265e23fe",
                "61b32d2516d501c9265e27b3",
                "61b32d2616d501c9265e2ddd",
                "61b32d2616d501c9265e2ff8",
                "61b32d2616d501c9265e30ab",
            ],
        };
        //navigate("/keyword", { state: result.data });
        navigate("/keyword", { state: result });
    };

    return (
        <div className="contents-wrapper">
            <h1>책 추천 해드립니다</h1>
            <h5>
                검색한 키워드와 유사한 책의 리뷰에서 키워드를 추출해 해당 키워드를 기반으로 순위를 매겨 책을
                추천해줍니다.
            </h5>
            <Paper
                style={{
                    width: "40rem",
                    borderRadius: "20px",
                    borderWidth: "1px",
                    borderStyle: "solid",
                    borderColor: "#ececec",
                }}
            >
                <form onSubmit={onSubmit} style={{ display: "flex", justifyContent: "center", alignItems: "center" }}>
                    <InputBase
                        fullwidth
                        defaultValue={keyword}
                        value={keyword}
                        style={{ width: "80%" }}
                        onChange={(e) => setKeyword(e.target.value)}
                    ></InputBase>

                    <IconButton type="submit">
                        <Search />
                    </IconButton>
                </form>
            </Paper>
        </div>
    );
};

export default Main;
