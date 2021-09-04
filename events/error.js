const moment = require("moment");

module.exports = {
    name: "error",
    active: true,
    execute(error) {
        console.log(`[ERROR] [${moment().format("M/D/Y - h:m:s A")}] ${error}`);
    }
}