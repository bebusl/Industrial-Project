const router = require("express").Router();
const Book = require("../model/book");
const ObjectId = require("mongoose").Types.ObjectId;

router.get("/:bookId", (req, res) => {
  const bookId = ObjectId(req.params.bookId);
  Book.findOne({ _id: bookId })
    .then((data) => {
      return res.json({
        success: true,
        msg: "책 정보 조회 성공",
        data: {
          title: data.name,
          author: data.author,
          price: data.price,
          detail: data.detail,
          reviews: data.reviews,
        },
      });
    })
    .catch((e) =>
      res.status(302).json({ success: false, msg: "책 정보 조회 실패" })
    );
});

module.exports = router;
