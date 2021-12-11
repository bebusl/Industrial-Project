import "./Nav.css";
import { Link } from "react-router-dom";
import withAuth from "../container/withAuth";
import { useEffect } from "react";
import axios from "axios";

function Nav({ isLogin, logoff, userData, history, login }) {
    useEffect(() => {
        axios
            .get("http://localhost:5000/auth/status")
            .then((res) => {
                if (res.status === 200) {
                    login(res.data.userData);
                } else {
                    logoff();
                }
            })
            .catch((e) => {
                console.log("NavErr ", e);
            });
    }, [isLogin]);

    return (
        <>
            <nav>
                <img src={`${process.env.PUBLIC_URL}/logo.svg`} alt="logo undefined" />;
                {!isLogin ? (
                    <ul>
                        <li>
                            <Link to="/">홈</Link>
                        </li>
                        <li>
                            <Link to="/login">로그인</Link>
                        </li>
                        <li>
                            <Link to="/register">회원가입</Link>
                        </li>
                    </ul>
                ) : (
                    <ul>
                        <li>
                            <Link to="/">홈</Link>
                        </li>
                        <li>
                            <a
                                href="#"
                                onClick={(e) => {
                                    e.preventDefault();
                                    axios
                                        .get("http://localhost:5000/auth/logout")
                                        .then((res) => {
                                            logoff();
                                            history.push("/");
                                        })
                                        .catch((e) => console.error(e));
                                }}
                            >
                                로그아웃
                            </a>
                        </li>
                        <li>
                            <Link to="/cart">{userData.name}님의 장바구니</Link>
                        </li>
                    </ul>
                )}
            </nav>
        </>
    );
}

export default withAuth(Nav);
