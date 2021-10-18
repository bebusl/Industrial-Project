const mongoose = require("mongoose");
const { Schema } = mongoose;

const root = encodeURI("root");

mongoose.connect(`mongodb://localhost:27017/book`, function (err, res) {
    if (res) {
        console.log(`DB연결성공 ${res}`);
    }
    if (err) {
        console.log(`DB연결실패 ${err}`);
    }
});
