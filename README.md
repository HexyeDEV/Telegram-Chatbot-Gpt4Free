# Telegram-Chatbot-Gpt4Free
This is a Python-based Telegram bot using the telethon library. The bot responds to messages using the GPT4FREE repo. This bot also supports plugins, roles, dan jailbreak and long term memory via vector database

# Installation
Clone the repo

```git clone https://github.com/HexyeDEV/Telegram-Chatbot-Gpt4Free.git```
After that go to the cloned repo directory.

Edit the example.env file with:

API_ID is your api id from https://my.telegram.org

API_HASH is your api hash from https://my.telegram.org

BOT_TOKEN is your bot token from Bot Father

If you want to use WalframAlpha plugin, you will need to create an app at https://products.wolframalpha.com/api/ and set WOLFRAMALPHA_APP_ID in the example.env to the APP_ID of your Wolfram apllication.

After that, rename example.env into .env.

Install all the packages running ```pip install -r requirements.txt```(may change based on your python version, settings and os.)

Now run main.py with ```python3 main.py```(may change based on your python version, settings and os.)

Enjoy!

# Commands:

/help - see a command list

/plugins toggle - enable/disable plugins

/plugins list - list all plugins

/newrole <Role Name> <Role Info> - create a new role

/roles - list all the roles

/role <Role Name> - enable a role

/role disable - disable roles

/memory - enable/disable memory

/addmemory - add something to the memory without receiving AI response.

# Provider Used

This project is using [GPT4FREE](https://github.com/xtekky/gpt4free)
