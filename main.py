from telethon import TelegramClient
from telethon.events import NewMessage
from dotenv import load_dotenv
from os import getenv
import json
from memory import Memory
from uuid import uuid4
from g4f import AsyncClient
from g4f.Provider import RetryProvider, ChatGptEs, DDG, Jmuz, Liaobots, OIVSCode, Pizzagpt, PollinationsAI
from process_plugins import process_plugins
from plugins import plugins as plugins_list
from roles import Role

load_dotenv()

memory = Memory('BotMemories')

api_id = getenv('API_ID')
api_hash = getenv('API_HASH')
bot_token = getenv('BOT_TOKEN')
wolframalpha_app_id = getenv('WOLFRAMALPHA_APP_ID')

if not api_id or not api_hash or not bot_token:
    raise Exception('API_ID, API_HASH and BOT_TOKEN must be set in .env file')

client = TelegramClient('bot', api_id, api_hash)
GPTClient = AsyncClient(
    provider=RetryProvider([ChatGptEs, DDG, Jmuz, Liaobots, OIVSCode, Pizzagpt, PollinationsAI], shuffle=True)
)

PLUGINS = False
MEMORY = False
ROLE = None

for plugin in plugins_list:
    plugins_string += f"\n{plugin.name}: {plugin.prompt}"

PLUGIN_PROMPT = f"You will be given a list of plugins with description. Based on what the plugin's description says, if you think a plugin is appropriate to use, answer with the instructions to use it. If no plugin is needed, do not mention them. The available plugins are: {plugins_string}"

def _format_text(text):
    text = text.replace("[[Login to OpenAI ChatGPT]]()", "")
    text = text.replace("\\[\n", "")
    text = text.replace("\\]", "")
    text = text.replace("\\n", "\n")
    text = text.replace("\\(", "(")
    text = text.replace("\\)", ")")
    return text

async def AiAgent(prompt, system_prompt=""):
    req = await GPTClient.chat.completions.create(model="gpt-4o-mini", messages=[{"content": system_prompt, "role": "system"},{"content": prompt, "role": "user"}])
    full_text = req.choices[0].message.content
    return _format_text(full_text)

@client.on(NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Hey! Write something and I will answer you using the gpt-4o-mini model or add me to a group and I will answer you when you mention me.')

@client.on(NewMessage(pattern='/help'))
async def help(event):
    await event.respond('Hey! Write something and I will answer you using the gpt-4o-mini model or add me to a group and I will answer you when you mention me.\nCommands:\n\n/plugins toggle - enable/disable plugins\n\n/plugins list - list all plugins\n\n/newrole <Role Name> <Role Info> - add a new role\n\n/roles - list all roles\n\n/role <Role Name> enable a role\n\n/role disable - disable roles\n\n/memory - enable/disable memory\n\n/addmemory - add something to the memory without receiving AI response.')

@client.on(NewMessage(pattern='/plugins list'))
async def pls(event):
    pls = []
    for plugin in  plugins_list:
        pls.append(plugin.name)
    await event.respond("Available plugins are:\n{}".format("\n".join(pls)))

@client.on(NewMessage(pattern='/plugins toggle'))
async def pls_toggle(event):
    global PLUGINS
    PLUGINS = not PLUGINS
    if PLUGINS == True and not wolframalpha_app_id or PLUGINS == True and wolframalpha_app_id == "TEST-APP":
        await event.respond("You need to set a wolframalpha app id in the .env file to use plugins.")
        PLUGINS = False
        return
    await event.respond("Plugins enabled" if PLUGINS == True else "Plugins disabled")

@client.on(NewMessage(pattern='/newrole'))
async def newrole(event):
    with open("roles.json", "r") as f:
        roles = f.read()
    roles = json.loads(roles)
    try:
        role_name = event.text.split(" ")[1]
        role = event.text.split(" ", 2)[2]
    except IndexError:
        await event.respond("You need to specify a role name and a role.")
        return
    roles[role_name] = role
    with open("roles.json", "w") as f:
        f.write(json.dumps(roles))
    await event.respond("Role added")

@client.on(NewMessage(pattern='/roles'))
async def roles(event):
    with open("roles.json", "r") as f:
        roles = f.read()
    roles = json.loads(roles)
    await event.respond("Available roles:\n{}".format("\n".join(roles.keys())))

@client.on(NewMessage(pattern='/role'))
async def role(event):
    global ROLE
    with open("roles.json", "r") as f:
        roles = f.read()
    roles = json.loads(roles)
    try:
        role = event.text.split(" ")[1]
    except IndexError:
        await event.respond("You need to specify a role.")
        return
    if role not in roles:
        await event.respond("Role not found.")
        return
    ROLE = Role(role, roles[role])
    await event.respond("Role enabled")

@client.on(NewMessage(pattern='/memory'))
async def memory_command(event):
    global MEMORY
    MEMORY = not MEMORY
    await event.respond("Memory enabled" if MEMORY == True else "Memory disabled")

@client.on(NewMessage(pattern='/addmemory'))
async def addmemory(event):
    global memory
    text = event.text.split(' ', 1)[1]
    memory.insert(text, str(uuid4()))
    await event.respond("Memory added")

@client.on(NewMessage())
async def message(event):
    global PLUGINS
    global MEMORY
    global ROLE
    my_id = await client.get_me()
    my_id = my_id.id
    my_username = await client.get_me()
    my_username = my_username.username
    if event.text.startswith("/"):
        return
    if not event.is_private:
         if not event.text.startswith(f'@{my_username}'):
            return
    prompt = event.text.replace(f'@{my_username}', '')
    if ROLE and PLUGINS:
        await event.respond("You can't use roles and plugins at the same time.")
        return
    msg = await event.respond("Thinking...")
    got_end_result = False
    system_prompt = ""
    if ROLE:
        system_prompt = ROLE.prompt
    if MEMORY:
        res = memory.find(prompt, 1)
        if len(res) > 0 and res != []:
            system_prompt = system_prompt + "To answer the next question these data may be relevant: " + res[0][0]
    if PLUGINS:
        result = await AiAgent(prompt, system_prompt)
        should_query, query = process_plugins(result)
        if should_query:
            result = await AiAgent(query, system_prompt)
        got_end_result = True
    if not got_end_result:
        result = await AiAgent(prompt, system_prompt)
    if MEMORY:
        memory.insert(prompt, str(uuid4))
        memory.insert(result, str(uuid4))
    await msg.edit(result)


client.start(bot_token=bot_token)
client.run_until_disconnected()