const fs = require("fs")

const { Client, Intents, Collection, Options, CommandInteraction } = require("discord.js");
const Hypixel = require("hypixel-api-reborn");
const { Pool } = require("pg");

const { keys } = require("../config.json");

const intents = new Intents(32767); // all intents
const client = new Client({ intents: intents, makeCache: Options.cacheEverything() });

console.log("[STARTUP] Initializing..")

client.commands = new Collection();
const commandFiles = fs.readdirSync("./commands").filter(file => file.endsWith(".js"));
console.log("[COMMANDS] Loading commands..")
for (const file of commandFiles) {
    const command = require(`./commands/${file}`);
    if (command.disabled) continue;
    client.commands.set(command.data.name, command);
    console.log(`[COMMANDS] /${command.data.name} loaded`)
};

const eventFiles = fs.readdirSync('./events').filter(file => file.endsWith('.js'));
console.log("[EVENTS] Registering events..")
for (const file of eventFiles) {
    const event = require(`./events/${file}`);
    if (event.disabled) continue;
    if (event.once) {
        client.once(event.name, (...args) => event.execute(...args));
        console.log(`[EVENTS] One time event ${event.name} registered`);
    } else {
        client.on(event.name, (...args) => event.execute(...args));
        console.log(`[EVENTS] Persistent event ${event.name} registered`);
    };
};

client.hypixel = new Hypixel.Client(keys.hypixel);

client.db = new Pool({
    user: "postgres",
    database: "umjibot",
    password: keys.postgres
});

console.log("[STARTUP] Logging into Discord..");
client.login(keys.token);
