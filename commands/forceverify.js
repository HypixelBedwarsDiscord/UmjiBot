const { SlashCommandBuilder } = require("@discordjs/builders");
const { MessageEmbed } = require("discord.js");
const { guildID, staffRoleID, verificationLogsChannelID } = require("../static");

module.exports = {
    data: new SlashCommandBuilder()
        .setName("forceverify")
        .setDescription("Force verifies user, giving appropriate roles, setting nickname, and saving UUID to database")
        .addUserOption(option =>
            option.setName("member")
                .setDescription("The member to force verify")
                .setRequired(true))
        .addStringOption(option =>
            option.setName("ign")
                .setDescription("The Minecraft IGN to force verify the specified member as")
                .setRequired(true)),

    async execute(interaction) {
        if (interaction.guild.id !== guildID) {
            return await interaction.reply({ content: "This command cannot be used here", ephemeral: true })
        }
        if (!interaction.member.roles.cache.has(staffRoleID)) {
            return await interaction.reply({ content: "You do not have sufficient permissions to use this command", ephemeral: true });
        }
        const member = interaction.guild.members.cache.get(interaction.options.getUser("member").id);
        const ign = interaction.options.getString("ign");
        let player;
        try {
            player = await interaction.client.hypixel.getPlayer(ign)
        } catch (error) {
            return await interaction.reply({ content: "IGN does not exist", ephemeral: true });
        }
        await interaction.client.verify(member, player)
        await interaction.reply({ content: `${member} has been verified`, ephemeral: true });
        if (!member.manageable) {
            await interaction.followUp({ content: `Missing permissions to set ${member}'s nickname`, ephemeral: true });
        };
        // save to database
        await interaction.client.db.query("INSERT INTO users(id, uuid) VALUES($1, $2) ON CONFLICT (id) DO UPDATE SET uuid = $2", [BigInt(member.id), player.uuid]);
        // log to channel
        const logEmbed = new MessageEmbed()
            .setTitle("Member Force Verified")
            .setColor("GREEN")
            .setTimestamp(interaction.createdTimestamp)
            .addFields(
                { name: "Member", value: `${member} (${member.user.username}#${member.user.discriminator}) [${member.id}]` },
                { name: "Moderator", value: interaction.member.toString() },
                { name: "Minecraft IGN", value: player.nickname }
            );
        await interaction.guild.channels.cache.get(verificationLogsChannelID).send({ embeds: [logEmbed] });
    }
};