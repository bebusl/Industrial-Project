import "./App.css";
import { Routes, Route } from "react-router-dom";
import { Main, Keyword, Ranking, Mypage, Book } from "./components/pages";
import axios from "axios";

function App() {
    return (
        <div className="App">
            <Routes>
                <Route path="/" element={<Main />}></Route>
                <Route path="/keyword" element={<Keyword />}></Route>
                <Route path="/ranking" element={<Ranking />}></Route>
                <Route path="/mypage" element={<Mypage />}></Route>
                <Route path="/book/:bookId" element={<Book />}></Route>
            </Routes>
        </div>
    );
}

export default App;
