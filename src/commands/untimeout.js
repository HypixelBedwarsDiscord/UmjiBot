const { SlashCommandBuilder } = require("@discordjs/builders");
const { MessageEmbed } = require("discord.js");
const { guildID, staffRoleID, timeoutLogsChannelID } = require("../static");

module.exports = {
    data: new SlashCommandBuilder()
        .setName("untimeout")
        .setDescription("Removes timeout from member")
        .addUserOption(option =>
            option.setName("member")
                .setDescription("The member to untimeout")
                .setRequired(true))
        .addStringOption(option =>
            option.setName("reason")
                .setDescription("The reason for the timeout")),

    async execute(interaction) {
        if (interaction.guild.id !== guildID) {
            return await interaction.reply({ content: "This command cannot be used here", ephemeral: true })
        }
        if (!interaction.member.roles.cache.has(staffRoleID)) {
            return await interaction.reply({ content: "You do not have sufficient permissions to use this command", ephemeral: true });
        }
        const member = interaction.guild.members.cache.get(interaction.options.getUser("member").id);
        if (!member) return await interaction.reply({ content: "Unknown member", ephemeral: true });
        if (!member.manageable) return await interaction.reply({ content: "Cannot untimeout this user", ephemeral: true });
        const reason = interaction.options.getString("reason") ? interaction.options.getString("reason") : "No reason given"
        await member.timeout(null);
        await interaction.reply(`Removed timeout from ${member}`);
        const logEmbed = new MessageEmbed()
            .setTitle("Member Timeout Removed")
            .setDescription(`${member}`)
            .addFields({
                name: "Reason", value: reason,
                name: "Moderator", value: `${interaction.member}`
            })
        await interaction.guild.channels.cache.get(timeoutLogsChannelID).send({ embeds: [logEmbed] });
    }
};