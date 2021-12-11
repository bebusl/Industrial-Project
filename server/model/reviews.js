const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const reviewSchema = new Schema({
    _id: Schema.Types.ObjectId,
    bookId: Schema.Types.ObjectId,
    review: { type: String, default: new Object() },
    analysis: Object,
    createdAt: { type: Date, expires: 60 * 60 * 1, default: Date.now },
});

const ReviewCollection = mongoose.model("Review", reviewSchema);

module.exports = ReviewCollection;
