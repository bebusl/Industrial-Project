const router = require("express").Router();
const User = require("../model/user");
const Wishlist = require("../model/wishilist");
const SearchKeyword = require("../model/searchKeyword");
const { jwtMiddleware } = require("./middlewares");

const findIds = async (id) => {
  const user = await User.findOne({ id });

  return {
    wishlistId: user["wishlist"],
    searchKeywordId: user["searchKeyword"],
  };
  //wishlistId는 ObjectId타입이므로 주의
};

router.get("/", jwtMiddleware, (req, res) => {
  const id = req.userEmail;
  const { wishlistId, searchKeywordId } = findIds(id);
  let data;
  try {
    let wishlists = await Wishlist.findOne({ _id: wishlistId });
    let searchkeywords = await SearchKeyword.findOne({ _id: searchKeywordId });
    data = {
      wishlists: wishlists["wishlists"],
      searchkeywords: searchkeywords["keywords"],
    };
    return res.json({
      success: true,
      data: data,
      msg: "데이터 조회에 성공했습니다",
    });
  } catch (e) {
    return res
      .status(302)
      .json({ success: false, msg: "db조회에 실패했습니다" });
  }
});

module.exports = router;
