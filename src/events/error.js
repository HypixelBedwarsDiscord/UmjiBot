const moment = require("moment");

module.exports = {
    name: "error",
    disabled: true,
    execute(error) {
        console.error(`[ERROR] [events/error.js] [${moment().format("M/D/Y - h:m:s A")}] ${error.stack}`);
    }
};