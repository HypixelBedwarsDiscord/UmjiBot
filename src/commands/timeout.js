const { SlashCommandBuilder, time } = require("@discordjs/builders");
const { MessageEmbed } = require("discord.js");
const { guildID, staffRoleID, timeoutLogsChannelID } = require("../static");

module.exports = {
    data: new SlashCommandBuilder()
        .setName("timeout")
        .setDescription("Gives member a timeout with the provided time and reason using the built-in Discord timeout feature")
        .addUserOption(option =>
            option.setName("member")
                .setDescription("The member to timeout")
                .setRequired(true))
        .addBooleanOption(option =>
            option.setName("dm")
                .setDescription("DMs the member being timed out about their punishment")
                .setRequired(true))
        .addStringOption(option =>
            option.setName("reason")
                .setDescription("The reason for the timeout"))
        .addIntegerOption(option =>
            option.setName("days")
                .setDescription("The number of days to timeout for"))
        .addIntegerOption(option =>
            option.setName("hours")
                .setDescription("The number of hours to timeout for"))
        .addIntegerOption(option =>
            option.setName("minutes")
                .setDescription("The number of minutes to timeout for")),

    async execute(interaction) {
        if (interaction.guild.id !== guildID) {
            return await interaction.reply({ content: "This command cannot be used here", ephemeral: true })
        }
        if (!interaction.member.roles.cache.has(staffRoleID)) {
            return await interaction.reply({ content: "You do not have sufficient permissions to use this command", ephemeral: true });
        }
        const member = interaction.guild.members.cache.get(interaction.options.getUser("member").id);
        if (!member) return await interaction.reply({ content: "Unknown member", ephemeral: true });
        if (!member.manageable) return await interaction.reply({ content: "Cannot timeout this user", ephemeral: true });
        const reason = interaction.options.getString("reason") ? interaction.options.getString("reason") : "No reason given"
        const days = interaction.options.getInteger("days");
        const hours = interaction.options.getInteger("hours");
        const minutes = interaction.options.getInteger("minutes");
        if (!days && !hours && !minutes) {
            return await interaction.reply({ content: "You must specify a time", ephemeral: true });
        }
        const duration = (days * 86400000) + (hours * 3600000) + (minutes * 60000);
        await member.timeout(duration, reason);
        await interaction.reply(`${member} has been timed out for ${getDurationString(days, hours, minutes)}`);
        let sentDM = "False";
        try {
            const DMembed = new MessageEmbed()
                .setTitle(`Timeout in ${interaction.guild.name}`)
                .addFields(
                    { name: "Duration", value: getDurationString(days, hours, minutes) },
                    { name: "Reason", value: reason }
                )
            await member.send({ embeds: [DMembed] });
            sentDM = "True";
        } catch (error) {
            sentDM = "False (Member has DMs turned off)"
            console.info(`[INFO] [commands/timeout.js] Cannot send DMs to ${member.user.username}#${member.user.discriminator}`);
        }
        const logEmbed = new MessageEmbed()
            .setTitle("Member Timed Out")
            .setDescription(`${member}`)
            .addFields(
                { name: "Duration", value: getDurationString(days, hours, minutes) },
                { name: "Reason", value: reason },
                { name: "Moderator", value: `${interaction.member}` },
                { name: "Sent DM", value: `${sentDM}` }
            )
        await interaction.guild.channels.cache.get(timeoutLogsChannelID).send({ embeds: [logEmbed] });
    }
};

function getDurationString(days, hours, minutes) {
    days = days ? `${days} day(s)` : ""
    hours = hours ? `${hours} hour(s)` : ""
    minutes = minutes ? `${minutes} minute(s)` : ""
    return [days, hours, minutes].filter((string) => !!string).join(", ")
}