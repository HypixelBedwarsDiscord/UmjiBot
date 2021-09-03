const { MessageEmbed } = require("discord.js");
const { guildID, verificationChannelID } = require("../static")

const welcomeEmbed = new MessageEmbed()
            .setTitle("Welcome to Hypixel Bedwars")
            .setDescription("Please follow the steps in the GIF shown, replacing the example Minecraft IGN (In Game Name) with **YOUR MINECRAFT IGN** to verify and gain access to the channels in this server. If you run into an issue, a staff member will assist you")
            .setColor("RANDOM")
            .setImage("https://static.myer.wtf/verificationguide.gif");

module.exports = {
    name: "guildMemberAdd",
    active: true,
    async execute(member) {
        if (member.guild.id !== guildID ) { 
            return; 
        };
        await member.send(`Please go to the <#${verificationChannelID}> channel in **Hypixel Bedwars** and follow the instructions in the channel`);
        await member.guild.channels.cache.get(verificationChannelID).send({ content: member.toString(), embeds: [welcomeEmbed] });
    }
}