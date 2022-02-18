module.exports = {
    name: "messageCreate",
    execute(message) {
        if (!message.nonce) {
            console.log(`[events/messageCreate.js] ${message.author.name}#${message.author.discriminator}: ${message.content} | nonce: ${message.nonce}`);
        }
    }
};