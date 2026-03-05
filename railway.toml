
require('dotenv').config();
const { Client, GatewayIntentBits, SlashCommandBuilder } = require('discord.js');
const { Rcon } = require('rcon-client');

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

async function sendRconCommand(command) {
    const rcon = await Rcon.connect({
        host: process.env.RCON_HOST,
        port: process.env.RCON_PORT,
        password: process.env.RCON_PASSWORD
    });

    await rcon.send(command);
    await rcon.end();
}

client.once('ready', async () => {
    console.log(`✅ Bot connecté : ${client.user.tag}`);

    const guild = await client.guilds.fetch(process.env.GUILD_ID);

    const commands = [
        new SlashCommandBuilder()
            .setName('revive')
            .setDescription('Revive un joueur')
            .addIntegerOption(option =>
                option.setName('id').setDescription('ID du joueur').setRequired(true)
            ),

        new SlashCommandBuilder()
            .setName('heal')
            .setDescription('Heal un joueur')
            .addIntegerOption(option =>
                option.setName('id').setDescription('ID du joueur').setRequired(true)
            ),

        new SlashCommandBuilder()
            .setName('ban')
            .setDescription('Ban un joueur')
            .addIntegerOption(option =>
                option.setName('id').setDescription('ID du joueur').setRequired(true)
            )
            .addStringOption(option =>
                option.setName('raison').setDescription('Raison du ban').setRequired(true)
            ),

        new SlashCommandBuilder()
            .setName('givecoins')
            .setDescription('Donner des coins à un joueur')
            .addIntegerOption(option =>
                option.setName('id').setDescription('ID du joueur').setRequired(true)
            )
            .addIntegerOption(option =>
                option.setName('amount').setDescription('Montant').setRequired(true)
            )
    ];

    for (const command of commands) {
        await guild.commands.create(command);
    }

    console.log("✅ Commandes Slash enregistrées !");
});

client.on('interactionCreate', async interaction => {
    if (!interaction.isChatInputCommand()) return;

    if (interaction.user.id !== process.env.ALLOWED_DISCORD_ID) {
        return interaction.reply({ content: "❌ Pas autorisé.", ephemeral: true });
    }

    try {
        if (interaction.commandName === 'revive') {
            const id = interaction.options.getInteger('id');
            await sendRconCommand(`revive ${id}`);
            await interaction.reply(`✅ Joueur ${id} revive.`);
        }

        if (interaction.commandName === 'heal') {
            const id = interaction.options.getInteger('id');
            await sendRconCommand(`heal ${id}`);
            await interaction.reply(`✅ Joueur ${id} heal.`);
        }

        if (interaction.commandName === 'ban') {
            const id = interaction.options.getInteger('id');
            const reason = interaction.options.getString('raison');
            await sendRconCommand(`ban ${id} ${reason}`);
            await interaction.reply(`🚫 Joueur ${id} banni. Raison: ${reason}`);
        }

        if (interaction.commandName === 'givecoins') {
            const id = interaction.options.getInteger('id');
            const amount = interaction.options.getInteger('amount');
            await sendRconCommand(`givecoins ${id} ${amount}`);
            await interaction.reply(`💰 ${amount} coins donnés au joueur ${id}.`);
        }

    } catch (err) {
        console.error(err);
        await interaction.reply("❌ Erreur lors de l'exécution.");
    }
});

client.login(process.env.DISCORD_TOKEN);

