const { MessageEmbed } = require("discord.js");
const { guildID, verificationChannelID, verificationLogsChannelID, needUsernamesRoleID } = require("../static");
const { verify } = require("../methods");

const welcomeEmbed = new MessageEmbed()
    .setTitle("Welcome to Hypixel Bedwars")
    .setDescription("Please follow the steps in the GIF shown, replacing the example Minecraft IGN (In Game Name) with **YOUR MINECRAFT IGN** to verify and gain access to the channels in this server. If you run into an issue, a staff member will assist you")
    .setColor("RANDOM")
    .setImage("https://static.myer.wtf/verificationguide.gif");

module.exports = {
    name: "guildMemberAdd",
    active: true,
    async execute(member) {
        if (member.guild.id !== guildID) return;
        const result = await member.client.db.query("SELECT * FROM users WHERE id = $1", [BigInt(member.id)]);
        if (result.rows[0]) {
            const uuid = result.rows[0].uuid
            let player;
            try {
                player = await member.client.hypixel.getPlayer(uuid)
            } catch (error) {
                return console.log(`[ERROR] [guildMemberAdd] UUID ${uuid} does not exist (This error should be impossible)`);
            }
            await verify(member, player);
            const logEmbed = new MessageEmbed()
                .setTitle("Member Verified Upon Join")
                .setColor("GREEN")
                .setTimestamp(member.joinedTimestamp)
                .addFields(
                    { name: "Member", value: `${member} (${member.user.username}#${member.user.discriminator}) [${member.id}]` },
                    { name: "Moderator", value: member.client.user.toString() },
                    { name: "Minecraft IGN", value: player.nickname }
                );
            member.guild.channels.cache.get(verificationChannelID).messages.fetch().then(async messages => {
                await member.guild.channels.cache.get(verificationChannelID).bulkDelete(messages.filter(m => m.mentions.has(member) && m.author.id === member.client.user.id));
            });
            return await member.guild.channels.cache.get(verificationLogsChannelID).send({ embeds: [logEmbed] });
        };
        try {
            await member.send(`Please go to the <#${verificationChannelID}> channel in **Hypixel Bedwars** and follow the instructions in the channel`);
        } catch (error) {
            console.log(`[INFO] [guildMemberAdd] Cannot send DMs to ${member.user.username}#${member.user.discriminator}`);
        }
        await member.roles.add(needUsernamesRoleID);
        await member.guild.channels.cache.get(verificationChannelID).send({ content: member.toString(), embeds: [welcomeEmbed] });
    }
};