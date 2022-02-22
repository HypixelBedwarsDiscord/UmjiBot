const moment = require("moment");

module.exports = {
    name: "ready",
    once: true,
    execute(client) {
        console.info(`[INFO] [events/ready.js] Connection established with Discord at ${moment().format("dddd, MMMM Do, Y - M/D/Y - h:m:s A")}`);
    }
}