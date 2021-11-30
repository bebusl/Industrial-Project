const router = require("express").Router();
const { jwtMiddleware } = require("./middlewares");
const Wishlist = require("../model/wishlist");
const User = require("../model/user");

const findWishlistId = async (id) => {
  const user = await User.findOne({ id });
  return user["wishlist"];
  //wishlistId는 ObjectId타입이므로 주의
};

//도서 찜. 도서 정보 "등록"이라 get보다 post를 쓰는 것이 맞지만 단순 uid만 전송하면 돼서 일단 get방식을 사용
router.get("/:id", jwtMiddleware, async (req, res) => {
  const id = req.userEmail;
  const bookId = req.params.id;
  const wishlistId = findWishlistId(id);
  Wishlist.updateOne({ _id: wishlistId }, { $push: { wishlists: bookId } })
    .then((success) => res.json({ success: true, msg: "찜을 성공했습니다." }))
    .catch((e) =>
      res.status(302).json({ success: false, msg: "찜 추가를 실패했습니다." })
    );
});

//도서 찜 삭제
router.delete("/:id", jwtMiddleware, async (req, res) => {
  const id = req.userEmail;
  const bookId = req.params.id;
  const wishlistId = findWishlistId(id);

  Wishlist.updateOne({ _id: wishlistId }, { $pull: { wishlists: bookId } })
    .then((success) =>
      res.json({ success: true, msg: "찜 삭제를 성공했습니다." })
    )
    .catch((e) =>
      res.status(302).json({ success: false, msg: "찜 삭제를 실패했습니다." })
    );
});

module.exports = router;
