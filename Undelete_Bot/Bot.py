import discord
import asyncio
import os.path as path
import datetime
import shelve
try:
    import Undelete_Bot.BotCommands.BotCommands as BotCommands
except ImportError:
    pass

try:
    import BotCommands as BotCommands
except ImportError:
    pass
bypassFile = 0

client = discord.Client()
# commands = BotCommands()
token = ''
servers = shelve.open('./Servers', writeback=True)


# Token
if path.isfile('./bot_token.txt'):
    with open('./bot_token.txt') as f:
        token = f.read()

if bypassFile == 1:
    token = ''

@client.event
async def on_ready():
    debugout("Logged in as")
    debugout(client.user.name)
    debugout(client.user.id)
    debugout('------')
    for i in servers:
        debugout(i)
        debugout(str(servers[i]))
        await client.send_message(destination=client.get_channel(str(servers[i])), content="Bot has been restarted on the host, Be aware that any message deletions to messages before this will not be displayed as the cache has been deleted by this action")

@client.event
async def on_message(message):
    if message.content.startswith('!ChanOut'):
        au = message.author
        if au.server_permissions.view_audit_logs:
            debugout(au.server_permissions)
            a = message.content
            a = a.split()
        # debugout("Chanout Split:" + a)
            if client.get_channel(a[1]):
                servers[str(message.server.id)] = a[1]
                servers.sync()
                await client.send_message(destination=client.get_channel(a[1]), content="Output set to this channel by: {0}".format(message.author))

@client.event
async def on_message_delete(message):
    debugout("Message-Deleted[server({0}) User({1}) Message({2})".format(message.server, message.author, message.content))
    user = message.author
    chan = message.channel
    outMessage = "User Has Deleted a Message [{0} AST]\n" \
                 "User: {1}\n" \
                 "User id: {4}\n" \
                 "Channel: {2}\n" \
                 "Content: ```{3}```".format(datetime.datetime.now(),  user.mention, chan.mention, str(message.content), message.author.id)


    c = servers[str(message.server)]
    await client.send_message(destination=client.get_channel(c), content=outMessage)

@client.event
async def raw_message_delete(message):
    pass


def debugout(message):
    print('[{0}] {1}'.format(datetime.datetime.now(), message))


client.run(token)