const { Client, Interaction, ApplicationCommandOptionType, PermissionFlagsBits } = require('discord.js');

module.exports = {
  /**
   *
   * @param {Client} client
   * @param {Interaction} interaction
   */

  callback: async (client, interaction) => {
    const amount = interaction.options.get('amount').value;

    if (amount < 1 || amount > 15) {
      await interaction.reply('Liczba wiadomości do usunięcia musi być między 1 a 15.');
      return;
    }

    

    try {
      await interaction.deferReply({ ephemeral: true });
      const messages = await interaction.channel.messages.fetch({ limit: amount });
      await interaction.channel.bulkDelete(messages);
      await interaction.followUp({ content: `${amount} wiadomości zostało usuniętych.`, ephemeral: false });
    } catch (error) {
      console.error(`Wystąpił błąd podczas usuwania wiadomości: ${error}`);
      await interaction.followUp('Wystąpił błąd podczas usuwania wiadomości.');
    }
  },

  name: 'clear',
  description: 'Deletes a certain amount of messages.',
  options: [
    {
      name: 'amount',
      description: 'Amount of messages to delete (1-15).',
      type: ApplicationCommandOptionType.Integer,
      required: true,
    },
  ],

  permissionsRequired: [PermissionFlagsBits.ManageMessages],
  botPermissions: [PermissionFlagsBits.ManageMessages],
};