module.exports = {
    name: "interactionCreate",
    async execute(interaction) {
        if (!interaction.isCommand) return;
        const command = interaction.client.commands.get(interaction.commandName);
        if (!command) return;

        try { 
            await command.execute(interaction);
        } catch (error) {
            console.error(error);
            try {
                await interaction.reply({ content: "This command failed!", ephemeral: true })
            } catch (error) {
                console.error(error)
            }
        }
    }
}