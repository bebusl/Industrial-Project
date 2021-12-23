import "./App.css";
import { Routes, Route } from "react-router-dom";
import Nav from "./components/layout/Nav";
import { Main, Keyword, Ranking, Mypage, Book, Login } from "./components/pages";
import axios from "axios";

function App() {
    return (
        <div className="App">
            <Nav />
            <Routes>
                <Route path="/" element={<Main />}></Route>
                <Route path="/keyword" element={<Keyword />}></Route>
                <Route path="/ranking" element={<Ranking />}></Route>
                <Route path="/mypage" element={<Mypage />}></Route>
                <Route path="/book/:bookId" element={<Book />}></Route>
                <Route path="/login" element={<Login />}></Route>
            </Routes>
        </div>
    );
}

export default App;
