const express = require("express");
const cors = require("cors");
const model = require("./model");
const authRouter = require("./routes/auth");
const recommendationRouter = require("./routes/recommendation");
const wishlistRouter = require("./routes/wishlist");
const userRouter = require("./routes/user");
const bookRouter = require("./routes/book");
const cookieParser = require("cookie-parser");
const swaggerUi = require("swagger-ui-express");
const bodyParser = require("body-parser");
const swaggerFile = require("./swagger-output");

const app = express();
const port = 5000;
const COOKIE_SECRET = require("./env").COOKIE_SECRET;

app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ limit: "50mb", extended: true }));
app.use(cookieParser(COOKIE_SECRET));
app.use(cors());

//router
app.use("/auth", authRouter);
app.use("/user", userRouter);
app.use("/wishlist", wishlistRouter);
app.use("/recommendation", recommendationRouter);
app.use("/book", bookRouter);

app.use("/swagger", swaggerUi.serve, swaggerUi.setup(swaggerFile));

//noRouter
app.use((req, res, next) => {
  const error = new Error(`${req.method} ${req.url} 라우터가 없습니다.`);
  error.status = 404;
  next(error);
});

//error handler
app.use((err, req, res, next) => {
  res.locals.message = err.message;
  res.locals.error = err;
  res.status(500);
  res.send("500", err.message);
});

app.listen(port, () => {
  console.log(`Service running at port ${port}`);
});
