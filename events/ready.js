module.exports = {
    name: "ready",
    once: true,
    active: true,
    execute(client) {
        console.log(`Connection established with Discord`);
    }
}