__Version__ = "1.2"
__Author__ = "Zachary Higgs"

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

# Use this to Bypass the File read if the token file refuses to work
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
    """
    Undelete
    :param message:
    :return:
    """
    debugout("Message-Deleted[server({0}) User({1}) Message({2})]".format(message.server, message.author, message.content))
    user = message.author
    chan = message.channel
    outMessage = "------------------------------------" \
                 "User Has Deleted a Message [{0} AST]\n" \
                 "User: {1}\n" \
                 "User id: {2}\n" \
                 "Channel: {3}\n" \
                 "Content: ```{4}```" \
                 "------------------------------------".format(datetime.datetime.now(),  user.mention, message.author.id ,chan.mention, str(message.content) )


    c = servers[str(message.server.id)]
    await client.send_message(destination=client.get_channel(c), content=outMessage)

@client.event
async def on_message_edit(message, after):
    debugout("Mesasage-Edit[server[{0} User({1} Message[{2}]".format(message.server, message.author, message.content))
    user = message.author
    chan = message.channel
    outMessage = "----------------------------------" \
                 "User has Edited a Message [{0}]\n" \
                 "User: {1}\n" \
                 "User id: {2}\n" \
                 "Channel: {3}\n" \
                 "Content before: ``` {4} ```\n" \
                 "Content After: ``` {5} ```" \
                 "----------------------------------".format(datetime.datetime.now(),  user.mention, message.author.id, chan.mention, str(message.content), str(after.content))
    c = servers[str(message.server.id)]
    await client.send_message(destination=client.get_channel(c), content=outMessage)

@client.event
async def raw_message_delete(message):
    pass


def debugout(message):
    print('[{0}] {1}'.format(datetime.datetime.now(), message))


client.run(token)
