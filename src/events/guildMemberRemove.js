const { guildID, verificationChannelID } = require("../static");

module.exports = {
    name: "guildMemberRemove",
    execute(member) {
        if (member.guild.id !== guildID) return;
        member.guild.channels.cache.get(verificationChannelID).messages.fetch().then(async messages => {
            await member.guild.channels.cache.get(verificationChannelID).bulkDelete(messages.filter(m => m.author.id === member.id || (m.mentions.has(member) && m.author.id === member.client.user.id) || (m.interaction && m.interaction.user.id === member.id)));
        });
    }
}