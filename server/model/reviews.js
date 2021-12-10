const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const reviewSchema = new Schema({
    _id: Schema.Types.ObjectId,
    bookId: Schema.Types.ObjectId,
    review: String,
    analysis: Object,
});

const ReviewCollection = mongoose.model("Review", reviewSchema);

module.exports = ReviewCollection;
