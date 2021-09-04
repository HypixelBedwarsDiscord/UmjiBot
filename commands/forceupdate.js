const { SlashCommandBuilder } = require("@discordjs/builders");
const { MessageEmbed } = require("discord.js");
const { guildID, staffRoleID, verificationLogsChannelID } = require("../static");
const { verify } = require("../methods");

module.exports = {
    data: new SlashCommandBuilder()
        .setName("forceupdate")
        .setDescription("Force update a member's roles and nickname based on Minecraft UUID from database")
        .addUserOption(option =>
            option.setName("member")
                .setDescription("The member to force update")
                .setRequired(true)
        ),

    async execute(interaction) {
        if (interaction.guild.id !== guildID) {
            return await interaction.reply({ content: "This command cannot be used here", ephemeral: true })
        }
        if (!interaction.member.roles.cache.has(staffRoleID)) {
            return await interaction.reply({ content: "You do not have sufficient permissions to use this command", ephemeral: true });
        }
        const member = interaction.guild.members.cache.get(interaction.options.getUser("member").id);
        const result = await interaction.client.db.query("SELECT * FROM users WHERE id = $1", [BigInt(member.id)]);
        let uuid;
        if (!result.rows[0] || result.rows[0].uuid === null) {
            return await interaction.reply({ content: `${member} is not verified`, ephemeral: true })
        } else {
            uuid = result.rows[0].uuid
        }
        let player;
        try {
            player = await interaction.client.hypixel.getPlayer(uuid)
        } catch (error) {
            return await interaction.reply({ content: "UUID does not exist (???)", ephemeral: true });
        }
        await verify(member, player)
        await interaction.reply({ content: `${member}'s roles and nickname have been updated`, ephemeral: true })
        if (!member.manageable) {
            await interaction.followUp({ content: `Missing permissions to set ${member}'s nickname`, ephemeral: true })
        };
        // log to channel
        const logEmbed = new MessageEmbed()
            .setTitle("Member Force Updated")
            .setColor("GREEN")
            .setTimestamp(interaction.createdTimestamp)
            .addFields(
                { name: "Member", value: `${member} (${member.user.username}#${member.user.discriminator}) [${member.id}]` },
                { name: "Moderator", value: interaction.member.toString() },
                { name: "Minecraft IGN", value: player.nickname }
            );
        await interaction.guild.channels.cache.get(verificationLogsChannelID).send({ embeds: [logEmbed] });
    }
}