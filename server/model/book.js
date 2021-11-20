const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const bookSchema = new Schema({
  _id: Schema.Types.ObjectId,
  name: { type: String, required: true },
  ISBN: String,
  author: String,
  price: Number,
  detail: String,
});
//id,password,nickname,wishilist

const BookCollection = mongoose.model("Book", bookSchema);

module.exports = bookCollection;
