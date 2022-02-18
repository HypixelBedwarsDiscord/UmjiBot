const moment = require("moment");

module.exports = {
    name: "ready",
    once: true,
    execute(client) {
        console.log(`[READY] Connection established with Discord at ${moment().format("dddd, MMMM Do, Y - M/D/Y - h:m:s A")}`);
    }
}