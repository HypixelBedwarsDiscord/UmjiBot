const moment = require("moment");

module.exports = {
    name: "interactionCreate",
    async execute(interaction) {
        if (!interaction.isCommand) return;
        const command = interaction.client.commands.get(interaction.commandName);
        if (!command) return;

        try { 
            await command.execute(interaction);
        } catch (error) {
            console.error(`[ERROR] [/${command.data.name}] [${moment().format("M/D/Y - h:m:s A")}] ${error.stack}`);
            if (!interaction.replied) await interaction.reply( {content: "This interaction failed", ephemeral: true });
        }
    }
}