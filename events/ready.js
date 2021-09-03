const moment = require("moment");

module.exports = {
    name: "ready",
    once: true,
    active: true,
    execute(client) {
        console.log(`[STARTUP] Connection established with Discord at ${moment().format("dddd, MMMM Do, Y - M/D/Y - h:m:s A")}`);
    }
}