const { SlashCommandBuilder } = require("@discordjs/builders");
const { guildID, staffRoleID } = require("../static");

module.exports = {
    enabled: true,
    data: new SlashCommandBuilder()
        .setName("purge")
        .setDescription("Purges messages from a channel")
        .addIntegerOption(option =>
            option.setName("messages")
                .setDescription("The number of messages to purge")
                .setRequired(true))
        .addChannelOption(option =>
            option.setName("channel")
                .setDescription("The channel to purge messages from. If not specificed, this will default to the current channel.")
        ),

    async execute(interaction) {
        if (interaction.guild.id !== guildID) return await interaction.reply({ content: "This command cannot be used here", ephemeral: true });
        if (!interaction.member.roles.cache.has(staffRoleID)) return await interaction.reply({ content: "You do not have sufficient permissions to use this command", ephemeral: true });
        let channel;
        if (!interaction.options.getChannel("channel")) channel = interaction.channel;
        else channel = interaction.options.getChannel("channel");
        channel.messages.fetch({ limit: interaction.options.getInteger("messages") }).then(async messages => await channel.bulkDelete(messages));
        await interaction.reply({ content: `Purged ${interaction.options.getInteger("messages")} ${interaction.options.getInteger("messages") > 1 ? 'messages' : 'message'} from ${channel}`, ephemeral: true });
    }
}