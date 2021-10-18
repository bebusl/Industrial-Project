const router = require("express").Router();
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");
const JWT_SECRET = require("../env").JWT_SECRET;
const User = require("../model/user");
const Wishlist = require("../model/wishilist");
const jwtMiddleware = require("./middlewares");
const ObjectId = require("mongoose").Types.ObjectId;
console.log("JWT_SECRET", JWT_SECRET);
const hashingPwd = async (password) => {
    let genSalt = await bcrypt.genSalt(10);
    let hashing = await bcrypt.hash(password, genSalt);
    return hashing;
}; //비밀번호 암호화

router.get("/", (req, res) => {
    res.send("Auth router test");
});

//회원가입
router.post("/register", (req, res) => {
    User.findOne({ id: req.body.id }).then(async (user) => {
        if (user) {
            return res.status(404).json({ msg: "해당 이메일을 가진 사용자가 이미 존재합니다." });
        } else {
            const newUser = new User({
                _id: new ObjectId(),
                id: req.body.id,
                nickname: req.body.nickname,
                password: req.body.password,
            });

            const wishlist = new Wishlist({
                uid: newUser._id,
                wishlists: [],
            });

            await hashingPwd(newUser.password)
                .then((hashing) => {
                    newUser.password = hashing;
                })
                .catch((err) => console.log("password hashing err :" + err));

            wishlist.save();
            newUser
                .save()
                .then((user) => res.json({ success: true, user: user }))
                .catch((err) => res.json({ success: false, msg: err }));
        }
    });
});

//로그인
router.post("/login", (req, res) => {
    const id = req.body.id;
    const password = req.body.password;

    User.findOne({ id }).then((user) => {
        if (!user) {
            const error = "해당하는 회원이 존재하지 않습니다.";
            return res.status(400).json({ errors: error });
        }

        bcrypt.compare(password, user.password).then((isMatch) => {
            if (isMatch) {
                const payload = { id: user.id, nickname: user.nickname };

                jwt.sign(payload, JWT_SECRET, { expiresIn: "7d" }, (err, token) => {
                    return res
                        .cookie("x_auth", token, { maxAge: 1000 * 60 * 60 * 24 * 7 })
                        .status(200)
                        .json({ success: true, userData: { id: user.id, nickname: user.nickname } });
                });
            } else {
                return res.status(400).json({ error: "패스워드가 일치하지 않습니다." });
            }
        });
    });
});

//로그아웃
router.get("/logout", jwtMiddleware, (req, res) => {
    console.log("TUREE");
    return res.cookie("x_auth", "").json({ success: true });
});

router.get("/status", jwtMiddleware, (req, res) => {
    return res.json({ success: true, userData: { id: req.id, nickname: req.nickname } });
});

module.exports = router;
