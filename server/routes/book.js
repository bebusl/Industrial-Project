const router = require("express").Router();
const Book = require("../model/book");
const ObjectId = require("mongoose").Types.ObjectId;

router.get("/:bookId", (req, res) => {
    const bookId = ObjectId(req.params.bookId);
    Book.findOne({ _id: bookId }, { title: 1, itemId: 1, author: 1, price: 1 })
        .then((data) => {
            return res.json({
                success: true,
                msg: "책 정보 조회 성공",
                data: {
                    _id: data._id,
                    title: data.title,
                    author: data.author,
                    price: data.price,
                    itemId: data.itemId,
                },
            });
        })
        .catch((e) => res.status(302).json({ success: false, msg: "책 정보 조회 실패" }));
});

module.exports = router;
