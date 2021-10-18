require("dotenv").config({ path: `${__dirname}/.env` });

const { env } = process;

module.exports = {
    ...env,
};
