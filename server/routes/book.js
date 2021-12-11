const router = require("express").Router();
const Book = require("../model/book");
const Review = require("../model/reviews");
const ObjectId = require("mongoose").Types.ObjectId;

router.get("/:bookId", async (req, res) => {
    const bookId = ObjectId(req.params.bookId);
    try {
        const t = await Book.findOne({ _id: bookId });
        const p = await Review.find({ bookId: bookId }, { _id: 0, review: 1, analysis: 1 });
        return res.json({
            success: true,
            msg: "책 정보 조회 성공",
            data: {
                book_info: t,
                reviews: p,
            },
        });
    } catch (e) {
        res.status(302).json({ success: false, msg: "책 정보 조회 실패" });
    }
});

module.exports = router;
