const { MessageActionRow, MessageButton } = require("discord.js");
const moment = require("moment");
const { staffRoleID, applicationCategoryChannelID } = require("../static");

module.exports = {
    name: "interactionCreate",
    async execute(interaction) {
        if (interaction.isCommand()) {
            const command = interaction.client.commands.get(interaction.commandName);
            if (!command) return;
            try { 
                await command.execute(interaction);
            } catch (error) {
                console.error(`[ERROR] [/${command.data.name}] [${moment().format("M/D/Y - h:m:s A")}] ${error.stack}`);
                if (!interaction.replied) await interaction.reply( {content: "This interaction failed", ephemeral: true });
            }
        } else if (interaction.isButton()) {
            if (interaction.customId === "closeApplicationChannel") {
                return await interaction.reply(`Application closed by <@${interaction.user.id}>`);
            } else if (interaction.customId === "deleteApplicationChannel") {
                if (!interaction.member.roles.cache.has(staffRoleID)) {
                    return await interaction.reply({ content: "You do not have sufficient permissions to use this command", ephemeral: true });
                }
                await interaction.deferUpdate();
                return await interaction.channel.delete();
            } else if (interaction.customId === "applicationStaff") {
                interaction.guild.channels.create(`staff-application-${interaction.user.username}`, { parent: applicationCategoryChannelID, permissionOverwrites: [
                    { id: interaction.user.id, allow: ["VIEW_CHANNEL", "SEND_MESSAGES"] },
                    { id: staffRoleID, allow: ["VIEW_CHANNEL", "SEND_MESSAGES"] },
                    { id: interaction.guild.id, deny: ["VIEW_CHANNEL", "SEND_MESSAGES"] }]  // role id of @everyone is the same as the guild id
                }).then(channel => {
                    interaction.reply( { ephemeral: true, content: `Application channel created: <#${channel.id}>`})
                    const row = new MessageActionRow()
                        .addComponents(
                            new MessageButton()
                                .setCustomId("closeApplicationChannel")
                                .setLabel("Close")
                                .setStyle("PRIMARY"), 
                            new MessageButton()
                                .setCustomId("deleteApplicationChannel")
                                .setLabel("Delete")
                                .setStyle("DANGER"))
                    channel.send({ content: "placeholder", components: [row] })
                })
            }
        }
    }
}