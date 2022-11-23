const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const wishlistSchema = new Schema({
  _id: Schema.Types.ObjectId,
  wishlists: { type: Schema.Types.Array, required: true },
});
//id,password,nickname,wishilist

const WishlistCollection = mongoose.model("Wishlist", wishlistSchema);

module.exports = WishlistCollection;
