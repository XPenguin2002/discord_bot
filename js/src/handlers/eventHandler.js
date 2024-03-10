const { TextChannel } = require('discord.js');
const path = require('path');
const getAllFiles = require('../utils/getAllFiles');

module.exports = (client) => {
  const eventFolders = getAllFiles(path.join(__dirname, '..', 'events'), true);

  for (const eventFolder of eventFolders) {
    let eventFiles = getAllFiles(eventFolder);
    eventFiles = eventFiles.sort();

    const eventName = eventFolder.replace(/\\/g, '/').split('/').pop();

    client.on(eventName, async (arg) => {
      for (const eventFile of eventFiles) {
        const eventFunction = require(eventFile);
        await eventFunction(client, arg);
      }
    });
  }

  client.on('guildMemberAdd', async (member) => {
    const welcomeChannel = member.guild.channels.cache.find(channel => channel.name === 'witaj');

    if (welcomeChannel instanceof TextChannel) {
      welcomeChannel.send(`${member} Elooo Elooo Mordeczko!`);
    }
  });

  client.on('raw', async (packet) => {
    if (!['GUILD_MEMBER_REMOVE'].includes(packet.t)) return;
  
    const { d: data } = packet;
    const guild = client.guilds.cache.get(data.guild_id);
  
    const farewellChannel = guild.channels.cache.find(channel => channel.name === 'witaj');
  
    if (farewellChannel instanceof TextChannel) {
      const user = data.user;
      farewellChannel.send(`${user.username} SPIERDOLIŁ, i tak był z niego tępy CHUJ!`);
    }
  });
};