import threading
import bot
import komendy

if __name__ == '__main__':
    bot_thread = threading.Thread(target=bot.run_discord_bot)
    komendy_thread = threading.Thread(target=komendy.run_discord_bot)

    bot_thread.start()
    komendy_thread.start()

    bot_thread.join()
    komendy_thread.join()