const fs = require("fs")
const { Client, Intents, Collection, Options } = require("discord.js");
const { keys } = require("./config.json");

const Hypixel = require("hypixel-api-reborn");
const { Pool } = require("pg");

const intents = new Intents(32767); // all intents
const client = new Client({ intents: intents, makeCache: Options.cacheEverything()});

client.commands = new Collection();
const commandFiles = fs.readdirSync("./commands").filter(file => file.endsWith(".js"));
for (const file of commandFiles) {
    const command = require(`./commands/${file}`);
    client.commands.set(command.data.name, command);
}

const eventFiles = fs.readdirSync('./events').filter(file => file.endsWith('.js'));
for (const file of eventFiles) {
    const event = require(`./events/${file}`);
    if (event.once) {
        client.once(event.name, (...args) => event.execute(...args));
    } else {
        client.on(event.name, (...args) => event.execute(...args));
    }
}

client.hypixel = new Hypixel.Client(keys.hypixel)

client.db = new Pool({
    user: "postgres",
    database: "umjibot",
    password: keys.postgres
})

const { verify, unverify } = require("./methods")
client.verify = verify
client.unverify = unverify

client.login(keys.token)