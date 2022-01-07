const { SlashCommandBuilder } = require("@discordjs/builders");
const { guildID, staffRoleID } = require("../static");

module.exports = {
    enabled: false,
    data: new SlashCommandBuilder()
        .setName("mute")
        .setDescription("Mutes member")
        .addUserOption(option =>
            option.setName("member")
                .setDescription("The member to mute")
                .setRequired(true))
        .addStringOption(option => 
            option.setName("duration")
                .setDescription("The amount of time to mute for"))
        .addStringOption(option => 
            option.setName("reason")
                .setDescription("The reason for the mute")),
    async execute(interaction) {
        if (interaction.guild.id !== guildID) return await interaction.reply({ content: "This command cannot be used here", ephemeral: true });
        if (!interaction.member.roles.cache.has(staffRoleID)) return await interaction.reply({ content: "You do not have sufficient permissions to use this command", ephemeral: true });
        const member = interaction.guild.members.cache.get(interaction.options.getUser("member").id);
        if (!member) return await interaction.reply({ content: "Unknown member", ephemeral: true });
    }
}