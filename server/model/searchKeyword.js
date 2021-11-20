const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const searchSchema = new Schema({
  _id: Schema.Types.ObjectId,
  keywords: { type: Schema.Types.Array, required: true },
});
//id,password,nickname,wishilist

const SearchKeywordCollection = mongoose.model("SearchKeyword", searchSchema);

module.exports = SearchKeywordCollection;
