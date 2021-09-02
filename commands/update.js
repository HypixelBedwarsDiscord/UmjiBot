const { SlashCommandBuilder } = require("@discordjs/builders");
const { MessageEmbed } = require("discord.js");
const { guildID, verificationLogsChannelID } = require("../static")

module.exports = {
    data: new SlashCommandBuilder()
        .setName("update")
        .setDescription("Update user roles and nickname based on Minecraft UUID from database"),
    async execute(interaction) {
        if (interaction.guild.id !== guildID) {
            return await interaction.reply({ content: "This command cannot be used here", ephemeral: true })
        }
        const result = await interaction.client.db.query("SELECT * FROM users WHERE id = $1", [BigInt(interaction.member.id)]);
        let uuid;
        if (!result.rows[0] || result.rows[0].uuid === null) {
            return await interaction.reply({ content: "You are not verified", ephemeral: true })
        } else {
            uuid = result.rows[0].uuid
        }
        let player;
        try {
            player = await interaction.client.hypixel.getPlayer(uuid)
        } catch (error) {
            return await interaction.reply({ content: "UUID does not exist (???)", ephemeral: true });
        }
        await interaction.client.verify(interaction.member, player);
        await interaction.reply({ content: "Your roles and nickname have been updated", ephemeral: true })
        if (!interaction.member.manageable) {
            await interaction.followUp({ content: "Missing permissions to set your nickname", ephemeral: true })
        };
        // log to channel
        const logEmbed = new MessageEmbed()
            .setTitle("Member Updated")
            .setColor("GREEN")
            .setTimestamp(interaction.createdTimestamp)
            .addFields(
                { name: "Member", value: `${interaction.member} (${interaction.member.user.username}#${interaction.member.user.discriminator}) [${interaction.member.id}]` },
                { name: "Moderator", value: interaction.client.user.toString() },
                { name: "Minecraft IGN", value: player.nickname }
            );
        await interaction.guild.channels.cache.get(verificationLogsChannelID).send({ embeds: [logEmbed] });
    }
}