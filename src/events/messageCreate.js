module.exports = {
    name: "messageCreate",
    execute(message) {
        if (!message.nonce && !message.author.bot) {
            console.log(`[events/messageCreate.js] #${message.channel.name}: ${message.author.username}#${message.author.discriminator}: ${message.content} | nonce: ${message.nonce}`);
        }
    }
};