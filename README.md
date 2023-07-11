# Some Setup Required

This README provides instructions on setting up and running a Discord bot with Rust+ connection. Follow the steps below to get started.

# Setting up the Discord bot

To set up a new Discord bot, follow these steps:

    Visit: https://discord.com/developers/applications
    Create a new application and give it a nifty name.
    Copy the application ID from the "General Information" section and paste it in the "config.json" file.
    In the "Bot" section, click "Add Bot."
    Copy the token after clicking "Reset Token" and paste it into the "config.json" file.

# Inviting the bot to your server.

To invite the bot to your server, do the following:

    Under "OAuth2," click "URL Generator."
    Select "BOT" in the options and tick the following permissions: "Send messages" and "Use Slash Commands."
    Go to the generated URL at the bottom and open it in your web browser.
    Follow the prompts to invite the bot to your designated server.

# Setting up the Rust+ connection information.

To set up the Rust+ connection information, follow these steps:

    Visit this website: https://rplus.ollieee.xyz/getting-started/getting-player-details
    Follow the instructions provided on the website.
    Copy the necessary information and paste it into the "config.json" file.

# Starting the Discord bot

To start the Discord bot, follow these steps:

    Press the Windows key, type "Command" or "CMD," and press Enter to open a command prompt.
    Open the folder where you saved the files from this repository.
    Copy the "URL" (well destination) and type: cd <destination> into the command prompt. For example: cd C:/users/gnomeslayer/desktop/vendingmachines/
    Install the necessary files by typing: pip install -r requirements.txt in the command prompt.
    Once the installation is complete, type python Discordbot.py to start the Discord bot.
