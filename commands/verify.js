const { SlashCommandBuilder } = require("@discordjs/builders");
const { MessageEmbed } = require("discord.js");
const { guildID, verificationLogsChannelID, verificationChannelID } = require("../static");

module.exports = {
    data: new SlashCommandBuilder()
        .setName("verify")
        .setDescription("Verifies user, giving appropriate roles, setting nickname, and saving UUID to database")
        .addStringOption(option =>
            option.setName("ign")
                .setDescription("The Minecraft IGN to verify as")
                .setRequired(true)),

    async execute(interaction) {
        if (interaction.guild.id !== guildID || interaction.channel.id !== verificationChannelID) {
            return await interaction.reply({ content: "This command cannot be used here", ephemeral: true })
        }
        const ign = interaction.options.getString("ign");
        let player;
        try {
            player = await interaction.client.hypixel.getPlayer(ign)
        } catch (error) {
            return await interaction.reply("IGN does not exist");
        }
        const hypixelDiscord = player.socialMedia.find(socialMedia => socialMedia.id === "DISCORD")
        // fail conditions
        if (!hypixelDiscord) {
            return await interaction.reply("No Discord tag linked on Hypixel");
        } else if (hypixelDiscord.link !== `${interaction.member.user.username}#${interaction.member.user.discriminator}`) {
            return await interaction.reply("Linked Discord tag on Hypixel does not match with your Discord tag");
        }
        // passed check
        await interaction.client.verify(interaction.member, player)
        await interaction.reply({ content: "You have been verified", ephemeral: true });
        if (!interaction.member.manageable) {
            await interaction.followUp({ content: "Missing permissions to set your nickname", ephemeral: true });
        };
        // save to database
        await interaction.client.db.query("INSERT INTO users(id, uuid) VALUES($1, $2) ON CONFLICT (id) DO UPDATE SET uuid = $2", [BigInt(interaction.member.id), player.uuid]);
        // log to channel
        const logEmbed = new MessageEmbed()
            .setTitle("Member Verified")
            .setColor("GREEN")
            .setTimestamp(interaction.createdTimestamp)
            .addFields(
                { name: "Member", value: `${interaction.member} (${interaction.member.user.username}#${interaction.member.user.discriminator}) [${interaction.member.id}]` },
                { name: "Moderator", value: interaction.client.user.toString() },
                { name: "Minecraft IGN", value: player.nickname }
            );
        await interaction.guild.channels.cache.get(verificationLogsChannelID).send({ embeds: [logEmbed] });
    }
};