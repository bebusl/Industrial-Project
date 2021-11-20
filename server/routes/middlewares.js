const jwt = require("jsonwebtoken");
const JWT_SECRET = require("../env").JWT_SECRET;
const User = require("../model/user");

const jwtMiddleware = async (req, res, next) => {
  let token = req.cookies.x_auth;
  if (!token || token.length == 0) {
    return res.status(501).json({ error: "저장된 token이 없습니다." });
  }
  await jwt.verify(token, JWT_SECRET, async (error, decoded) => {
    if (error) {
      return res
        .status(500)
        .json({ error: "token을 decode하는데 실패했습니다." });
    }
    console.log(decoded);
    await User.findOne({ id: decoded.id }, (error, user) => {
      if (error) {
        return res.json({
          error: "DB에서 회원정보를 찾는 도중 오류가 발생했습니다.",
        });
      }
      if (!user) {
        return res
          .status(400)
          .json({ isAuth: false, error: "token에 해당하는 유저가 없습니다." });
      }
      if (user) {
        req.userEmail = user.id;
        req.name = user.nickname;
      }
    }).catch((e) => console.error(e));
  });
  next();
};

const isLogin = async (req, res, next) => {
  let token = req.cookies.x_auth;
  if (!token || token.length == 0) {
    req.isLogin = false;
  }
  await jwt.verify(token, JWT_SECRET, async (error, decoded) => {
    if (error) {
      return res
        .status(500)
        .json({ error: "token을 decode하는데 실패했습니다." });
    }
    console.log(decoded);
    await User.findOne({ id: decoded.id }, (error, user) => {
      if (error) {
        return res.json({
          error: "DB에서 회원정보를 찾는 도중 오류가 발생했습니다.",
        });
      }
      if (!user) {
        return res
          .status(400)
          .json({ isAuth: false, error: "token에 해당하는 유저가 없습니다." });
      }
      if (user) {
        req.isLogin = true;
        req.userEmail = user.id;
        req.name = user.nickname;
      }
    }).catch((e) => console.error(e));
  });
  next();
};

module.exports = { jwtMiddleware, isLogin };
