const { SlashCommandBuilder } = require("@discordjs/builders");
const { MessageEmbed } = require("discord.js");
const { ownerID } = require("../static")

module.exports = {
    data: new SlashCommandBuilder()
        .setName("eval")
        .setDescription("haha nice try")
        .addStringOption(option =>
            option.setName("code")
                .setDescription("code")
                .setRequired(true)),

    async execute(interaction) {
        if (interaction.member.id !== ownerID) {
            return await interaction.reply({ content: "haha nice try", ephemeral: true });
        };
        client = interaction.client; // for the accessible variables in the eval
        const _code = interaction.options.getString("code");
        try {
            _result = eval(_code);
        } catch (_error) {
            const _replyEmbed = new MessageEmbed()
                .setTimestamp(interaction.createdTimestamp)
                .addFields(
                    { name: "Input", value: `\`\`\`${_code}\`\`\``},
                    { name: "Error", value: `\`\`\`${_error}\`\`\``}
                );
            return await interaction.reply({ embeds: [_replyEmbed], ephemeral: true });
        }
        const _replyEmbed = new MessageEmbed()
            .setTimestamp(interaction.createdTimestamp)
            .addFields(
                { name: "Input", value: `\`\`\`${_code}\`\`\``},
                { name: "Output", value: `\`\`\`${_result}\`\`\``}
            );
        await interaction.reply({ embeds: [_replyEmbed], ephemeral: true });
    }
}