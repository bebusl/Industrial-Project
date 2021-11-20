const router = require("express").Router();
const User = require("../model/user");
const SearchKeyword = require("../model/searchKeyword");
const { isLogin } = require("./middlewares");

//처음 검색
router.get("/:searchKeyword", isLogin, (req, res) => {
  const { search } = req.params;
  if (req.isLogin) {
    const id = req.userEmail;
    const user = await User.findOne({ id });
    SearchKeyword.updateOne(
      { _id: user["searchKeyword"] },
      { $push: { keywords: search } }
    );
  } //로그인 되어 있을 시 searchKeyword에 추가

  /*Update this.rabbitmq 연결하고 키워드 받아오는 거 추가*/

  return res.json({
    success: true,
    keywords: ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
  });
});

//키워드 선택
router.post("/keywords", (req, res) => {
  //모델 서버에 보내기. 코드 추가

  return res.json({
    success: true,
    data: [{ title: "book1" }, { title: "book2" }],
  }); //임시 response
});

module.exports = router;
