const moment = require("moment");
const { SlashCommandBuilder } = require("@discordjs/builders");
const { MessageEmbed } = require("discord.js");
const { guildID, verificationLogsChannelID, verificationChannelID } = require("../static");
const { verify, ignDoesNotExistEmbed } = require("../methods");

const discordNotLinkedOrNotMatchingEmbed = new MessageEmbed()
    .setTitle("Discord tag on Hypixel not linked or does not match")
    .setDescription("To set your Discord tag on Hypixel, please follow the instructions in the GIF below, **making sure to replace the example Discord tag of `myer#0001` with your own**")
    .setColor("DARK_RED")
    .setImage("https://static.myer.wtf/linkhypixeldiscordguide.gif")

function accountAlreadyVerifiedEmbed(ign, member) {
    return new MessageEmbed()
        .setTitle("Account already verified")
        .setDescription(`The IGN \`${ign}\` is already verified to another Discord account (${member}). If you believe this is an error, please ping a staff member`)
        .setColor("DARK_RED")
};

module.exports = {
    data: new SlashCommandBuilder()
        .setName("bwverify")
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
            console.info(`[DEBUG] [commands/bwverify.js] [${moment().format("M/D/Y - h:m:s A")}] ${error.stack}`);
            return await interaction.reply({ embeds: [ignDoesNotExistEmbed(ign)] });
        }
        // check if given ign (uuid) already in database
        const result = await interaction.client.db.query("SELECT * FROM users WHERE uuid = $1", [player.uuid])
        if (result.rows[0]) {
            // check if user is in the guild
            try {
                const member = await interaction.guild.members.fetch(result.rows[0].id);
                if (member.id !== interaction.member.id) {
                    console.log(
                        `[commands/bwverify.js] Failed verification attempt by ${interaction.member.user.username}#${interaction.member.user.discriminator}\n` +
                        `[commands/bwverify.js] UUID ${result.rows[0].uuid} already verified to member ${result.rows[0].id}`
                    )
                    return await interaction.reply({ embeds: [accountAlreadyVerifiedEmbed(player.nickname, member)] });
                }
            } catch (error) {  // error here means that the user is no longer in the guild
                console.log(
                    `[commands/bwverify.js] UUID ${result.rows[0].uuid} was already verified to member ${result.rows[0].id} but they are no longer in the guild\n` +
                    `[commands/bwverify.js] Removing ${result.rows[0].id} from database`
                )
                await interaction.client.db.query("DELETE FROM users WHERE id = $1", [BigInt(result.rows[0].id)]);
            };
        };
        const hypixelDiscord = player.socialMedia.find(socialMedia => socialMedia.id === "DISCORD")
        // fail conditions
        if (!hypixelDiscord) {
            return await interaction.reply({ embeds: [discordNotLinkedOrNotMatchingEmbed] });
        } else if (hypixelDiscord.link !== `${interaction.member.user.username}#${interaction.member.user.discriminator}`) {
            return await interaction.reply({ embeds: [discordNotLinkedOrNotMatchingEmbed] });
        }
        // passed check
        await verify(interaction.member, player)
        // save to database
        await interaction.client.db.query("INSERT INTO users(id, uuid) VALUES($1, $2) ON CONFLICT (id) DO UPDATE SET uuid = $2", [BigInt(interaction.member.id), player.uuid]);
        // reply
        await interaction.reply({ content: "You have been verified", ephemeral: true });
        if (!interaction.member.manageable) {
            await interaction.followUp({ content: "Missing permissions to set your nickname", ephemeral: true });
        };
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
        // delete join messages and messages from verified member in verification channel
        interaction.guild.channels.cache.get(verificationChannelID).messages.fetch().then(async messages => {
            await interaction.guild.channels.cache.get(verificationChannelID).bulkDelete(messages.filter(m => m.author.id === interaction.member.id || (m.mentions.has(interaction.member) && m.author.id === interaction.client.user.id) || (m.interaction && m.interaction.user.id === interaction.member.id)));
        });
    }
};
