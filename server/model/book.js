const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const bookSchema = new Schema({
    _id: Schema.Types.ObjectId,
    title: { type: String, required: true },
    isbn: String,
    isbn13: String,
    itemId: String,
    intro: String,
    contents: String,
    author: String,
    price: String,
    index: Number,
});
//id,password,nickname,wishilist

const BookCollection = mongoose.model("Book", bookSchema);

module.exports = BookCollection;
