const { SlashCommandBuilder } = require("@discordjs/builders");
const { MessageActionRow, MessageButton } = require("discord.js");
const { devChannelID } = require("../static");

module.exports = {
    data: new SlashCommandBuilder()
        .setName("dev")
        .setDescription("Whatever developer command I need at the time"),
    async execute(interaction) {
        const row = new MessageActionRow()
            .addComponents(
                    new MessageButton()
                        .setCustomId("applicationStaff")
                        .setLabel("Staff")
                        .setStyle("PRIMARY")
            )
        await interaction.guild.channels.cache.get(devChannelID).send({ content: "Select the position you would like to apply for", components: [row]});
    }
}