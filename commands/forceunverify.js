const { SlashCommandBuilder } = require("@discordjs/builders");
const { MessageEmbed } = require("discord.js");
const { guildID, staffRoleID, verificationLogsChannelID } = require("../static");

module.exports = {
    data: new SlashCommandBuilder()
        .setName("forceunverify")
        .setDescription("Force unverifies user, removing appropriate roles, resetting nickname, and remove UUID from database")
        .addUserOption(option =>
            option.setName("member")
                .setDescription("The member to force unverify")
                .setRequired(true)),

    async execute(interaction) {
        if (interaction.guild.id !== guildID) {
            return await interaction.reply({ content: "This command cannot be used here", ephemeral: true })
        }
        if (!interaction.member.roles.cache.has(staffRoleID)) {
            return await interaction.reply({ content: "You do not have sufficient permissions to use this command", ephemeral: true });
        }
        const member = interaction.guild.members.cache.get(interaction.options.getUser("member").id);
        await interaction.client.unverify(member);
        await interaction.reply({ content: `${member} has been force unverified`, ephemeral: true });
        if (!member.manageable) {
            await interaction.followUp({ content: `Missing permissions to reset ${member}'s nickname`, ephemeral: true });
        };
        // remove from database
        await interaction.client.db.query("DELETE FROM users WHERE id = $1", [BigInt(member.id)]);
        // log to channel
        const logEmbed = new MessageEmbed()
            .setTitle("Member Force Unverified")
            .setColor("YELLOW")
            .setTimestamp(interaction.createdTimestamp)
            .addFields(
                { name: "Member", value: `${member} (${member.user.username}#${member.user.discriminator}) [${member.id}]` },
                { name: "Moderator", value: interaction.member.toString() }
            );
        await interaction.guild.channels.cache.get(verificationLogsChannelID).send({ embeds: [logEmbed] });
    }
};