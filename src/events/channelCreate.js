const { ticketCategoryChannelID, supportTeamRoleID } = require("../static");

module.exports = {
    name: "channelCreate",
    async execute(channel) {
        if (channel.parentId !== ticketCategoryChannelID || !channel.name.startsWith("ticket-")) {
            return;
        };
        await channel.send(`<@&${supportTeamRoleID}>`);
    }
}