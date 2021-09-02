const { keys } = require("./config.json");
const { stars } = require("./prestiges");
const { roleIDs } = require("./prestiges")
const { needUsernamesRoleID, verifiedRoleID, hypixelStaffRoleID } = require("./static")

module.exports = {
    async verify(member, player) {
        let index = player.stats.bedwars.level / 100 | 0;
        index = index > 30 ? 30 : index;
        const role = roleIDs[index]
        // set nickname
        if (member.manageable) {
            const star = player.stats.bedwars.level.toString().length < 2 ? `0${player.stats.bedwars.level}` : player.stats.bedwars.level
            await member.setNickname(`[${star} ${stars[index]}] ${player.nickname}`);
        };
        // remove incorrect prestige roles
        if (!member.roles.cache.has(role)) {
            for (const role of roleIDs) {
                if (!member.roles.cache.has(role)) continue;
                await member.roles.remove(role);
            };
            // add correct prestige role
            await member.roles.add(role);
        };
        // hypixel staff roles (not yet fully sure how this works yet)
        // if (player.rank.equals("Admin") || player.rank.equals("Game Master")) {
            
        // };
        await member.roles.remove(needUsernamesRoleID);
        await member.roles.add(verifiedRoleID);
    },
    
    async unverify(member) {
        for (const role of roleIDs) {
            if (!member.roles.cache.has(role)) continue;
            await member.roles.remove(role);
        }
        await member.roles.add(needUsernamesRoleID);
        await member.roles.remove(verifiedRoleID);
        await member.setNickname(null);
    }
}