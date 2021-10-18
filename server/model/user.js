const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const userSchema = new Schema({
    _id: Schema.Types.ObjectId,
    id: { type: String, unique: true, required: true },
    password: { type: String, required: true },
    nickname: { type: String, required: true },
});
//id,password,nickname,wishilist

const UserCollection = mongoose.model("User", userSchema);

module.exports = UserCollection;
