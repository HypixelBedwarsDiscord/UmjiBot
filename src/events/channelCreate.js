const { ticketCategoryChannelID, supportTeamRoleID } = require("../static");

module.exports = {
    name: "channelCreate",
    active: true,
    async execute(channel) {
        if (channel.parentId !== ticketCategoryChannelID || !channel.name.startsWith("ticket-")) {
            return;
        };
        await channel.send(`<@&${supportTeamRoleID}>`);
    }
}