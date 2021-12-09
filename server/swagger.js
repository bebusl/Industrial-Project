const swaggerAutogen = require("swagger-autogen")();

const options = {
  definition: {
    openapi: "3.0.0",
    info: {
      title: "도서추천서비스 API",
      version: "0.1.0",
      description: "익스프레스로 만들어진 간단한 CRUD api",
      license: { name: "MIT", url: "https://spdx.org/licenses/MIT.html" },
      contact: {
        name: "도서추천서비스",
        url: "http://localhost:3000",
        email: "brill_be@naver.com",
      },
    },
    // servers: [{}],
  },
  apis: [
    "./routes/auth.js",
    "./routes/book.js",
    "./routes/recommendation.js",
    "./routes/user.js",
    "./routes/wishlist.js",
  ],
};

const outputFile = "./swagger-output.json";
const endpointsFiles = ["./index.js"];

swaggerAutogen(outputFile, endpointsFiles, options);
