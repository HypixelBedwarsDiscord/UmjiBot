const { MessageEmbed } = require("discord.js");
const { copypastaLogsChannelID, scamLinkLogsChannelID } = require("../static");

module.exports = {
    name: "messageCreate",
    async execute(message) { 
        // scam link
        if (message.author.bot) return;
        if (!message.nonce && !message.author.bot && message.type === "DEFAULT") {
            console.log(`[events/messageCreate.js] #${message.channel.name}: ${message.author.username}#${message.author.discriminator}: ${message.content} | nonce: ${message.nonce}`);
            const embed = new MessageEmbed()
                .setTitle("Scam Link Deleted")
                .addFields(
                    { name: "Author", value: `<@${message.author.id}> (${message.author.username}#${message.author.discriminator})` },
                    { name: "Content", value: message.content || "no message content" },
                    { name: "Channel", value: `<#${message.channel.id}>` }
                )
            await message.guild.channels.cache.get(scamLinkLogsChannelID).send({ embeds: [embed] });
            return await message.delete();
        }
        // copypasta
        // const lastThreeRepeatedMessages = (await message.channel.messages.fetch({ limit: 6})).filter(m => m.id !== message.id && m.content === message.content);
        // if (lastThreeRepeatedMessages.size >= 2) {
        //    const embed = new MessageEmbed()
        //        .setTitle("Copypasta Deleted")
        //        .addFields(
        //            { name: "Author", value: `<@${message.author.id}> (${message.author.username}#${message.author.discriminator})` },
        //            { name: "Content", value: message.content || "no message content" },
        //            { name: "Channel", value: `<#${message.channel.id}>` },
        //            { name: "Count", value: lastThreeRepeatedMessages.size.toString()}
        //        )
        //    await message.guild.channels.cache.get(copypastaLogsChannelID).send({ embeds: [embed] });
        //    return await lastThreeRepeatedMessages.each(m => m.delete());
        // }
    }
};
