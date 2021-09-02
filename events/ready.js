module.exports = {
    name: "ready",
    once: true,
    execute(client) {
        console.log(`Connection established with Discord`);
    }
}