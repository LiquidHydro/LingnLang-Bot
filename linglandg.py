import discord
import asyncio


client = discord.Client()
game = discord.Game(name="/help", url="", type=0)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_status(game=game)
    print('------')


@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.server.channels, name='what-is-your-native-language')
    destination_channel = discord.utils.get(member.server.channels, name='info')
    await client.send_message(channel, "Welcome {}! I am the motherbot of this server. If you need help with getting tags, I can apply them to you. To see my commands you can type `/help`. To get your required native tag, you can type `/native [your language]` example : `/native english` (all lowercase). After that, apply your `/studying` tag.".format(member.mention))

@client.event
async def on_message(message):
    if message.content.startswith('/help'):
        msg = "**Commands :**\n"
        msg = msg + '```'
        msg = msg +"/native [language]\n"
        msg = msg +"    Select your native language\n"
        msg = msg +"    example : /native english\n\n"
        msg = msg +"/fluent [language]\n"
        msg = msg +"    Select a language you are fluent in\n"
        msg = msg +"    example : /fluent english\n\n"
        msg = msg +"/studying [language]\n"
        msg = msg +"    Select a language you are studying\n"
        msg = msg +"    example : /studying english\n\n"
        msg = msg +"/notstudying [language]\n"
        msg = msg +"    remove a langauge stying tag\n"
        msg = msg +"    example : /notstudying english\n\n"
        msg = msg +"/whostudies [language]\n"
        msg = msg +"    Show who studies a language\n\n"
        msg = msg +"/whonative [language]\n"
        msg = msg +"    Show who is native in a language\n\n"
        msg = msg +"/whofluent [language]\n"
        msg = msg +"    Show who is fluent in a language\n\n"
        msg = msg +"/languages\n"
        msg = msg +"    Show the native languages that\n"
        msg = msg +"    aleady exist on the server"
        msg = msg + '```'
        await client.send_message(message.channel, msg)

    if message.content.startswith('/pat'):
        await client.send_message(message.channel, "https://media.giphy.com/media/12hvLuZ7uzvCvK/giphy.gif")

    if message.content.startswith('/hug'):
        arguments = (message.content.split(' ')[1:])
        msg = 'Hey '
        if len(message.mentions) == 1 and len(arguments) == 1:
            bot = discord.utils.get(message.server.members, name='Ling & Lang')
            if message.mentions[0] == message.author:
                msg = "Are you a neet?! here's a hug (つ｡◕‿‿◕｡)つ"
            elif message.mentions[0] == bot:
                msg = "I love me, *hugs* (つ｡◕‿‿◕｡)つ"
            else:
                msg = "{}{}! Here's a hug from {} (つ｡◕‿‿◕｡)つ \n".format(msg, message.mentions[0].mention, message.author.mention)
        elif len(message.mentions) > 1 and len(arguments) == len(message.mentions):
            for member in message.mentions:
                msg = '{}{} '.format(msg, member.mention)
            msg = "{}! Here's a hug from {} (つ｡◕‿‿◕｡)つ \n".format(msg, message.author.mention)

        await client.send_message(message.channel, msg)

    if message.content.startswith('/native'):
        arguments = (message.content.split(' ')[1:])

        if len(arguments) == 0:
            await client.send_message(message.channel, "How to use :\n\t/native [language]\n\nExample:\n\t/native english\n\nYou can use `/languages` to see the tags that already exist on the server. Even if your language is not on the list you can try it.")

            #verify if there are roles for the argument languages
        else:

            role = discord.utils.get(message.server.roles, name=arguments[0].lower().capitalize()+" native")
            if role != None:
                try:
                    await client.add_roles(message.author, role)
                    await client.send_message(message.channel, ""+message.author.mention+" you have been tagged with @"+ role.name)
                except discord.Forbidden:
                    print("forbidden")
                    await client.send_message(message.channel, "Oops! something went wrong, I should tell the Mods");
                except discord.HTTPException:
                    print("forbidden")
                    await client.send_message(message.channel, "Oops! something went wrong, I should tell the Mods");
            else:
                channel = discord.utils.get(message.server.channels, name="circlejerk")
                await client.send_message(channel,"Hey, just wanted to tell you that, "+message.author.mention+" Says that he is native in "+arguments[0].lower().capitalize())
                await client.send_message(message.channel, "This language is not on the list yet.\nI will ask the moderators to add it! It will be added soon (if they stop being lazy)\n\nIf you've made a mistake, type `/native` to see how to use the command.")

    if message.content.startswith('/languages'):
        await client.send_message(message.channel, languages_list(message.server))

    if message.content.startswith('/notstudying'):
        arguments = (message.content.split(' ')[1:])

        if len(arguments) == 0:
            await client.send_message(message.channel, "How to use :\n\t/notstudying [language]\n\nExample:\n\t/notstudying english")
        else:
            role = discord.utils.get(message.author.roles, name="Studying "+arguments[0].lower().capitalize())
            if role != None:
                try:
                    await client.remove_roles(message.author, role)
                    await client.send_message(message.channel, ""+message.author.mention+" I removed the tag @"+ role.name)
                except discord.Forbidden:
                    print("forbidden")
                    await client.send_message(message.channel, "Oops! something went wrong, I should tell the Mods");
                except discord.HTTPException:
                    print("httpexception")
                    await client.send_message(message.channel, "Oops! something went wrong, I should tell the Mods");
            else:
                #role not found
                await client.send_message(message.channel, "You are not studying this language!")
                

    if message.content.startswith('/studying'):
        arguments = (message.content.split(' ')[1:])
        if len(arguments) == 0:
            await client.send_message(message.channel, "How to use :\n\t/studying [language]\n\nExample:\n\t/studying english\n")
        else:
            role = discord.utils.get(message.server.roles, name="Studying "+arguments[0].lower().capitalize())
            if role != None:
                try:
                    await client.add_roles(message.author, role)
                    await client.send_message(message.channel, ""+message.author.mention+" you have been tagged with @"+ role.name)
                except discord.Forbidden:
                    print("forbidden")
                    await client.send_message(message.channel, "Oops! something went wrong, I should tell the Mods");
                except discord.HTTPException:
                    print("forbidden")
                    await client.send_message(message.channel, "Oops! something went wrong, I should tell the Mods");
            else:
                channel = discord.utils.get(message.server.channels, name="circlejerk")
                await client.send_message(channel,"Hey, just wanted to tell you that, "+message.author.mention+" Says that he is Studying "+arguments[0].lower().capitalize())
                await client.send_message(message.channel, "This language is not on the list yet.\nI will ask the moderators to add it! It will be added soon (if they stop being lazy)\n\nIf you've made a mistake, type `/studying` to see how to use the command.")
    if message.content.startswith('/fluent'):
        arguments = (message.content.split(' ')[1:])
        if len(arguments) == 0:
            await client.send_message(message.channel, "How to use :\n\t/fluent [language]\n\nExample:\n\t/fluent english\n")
        else:
            role = discord.utils.get(message.server.roles, name="Fluent in "+arguments[0].lower().capitalize())
            if role != None:
                try:
                    await client.add_roles(message.author, role)
                    await client.send_message(message.channel, ""+message.author.mention+" you have been tagged with @"+ role.name)
                except discord.Forbidden:
                    print("forbidden")
                    await client.send_message(message.channel, "Oops! something went wrong, I should tell the Mods");
                except discord.HTTPException:
                    print("forbidden")
                    await client.send_message(message.channel, "Oops! something went wrong, I should tell the Mods");
            else:
                channel = discord.utils.get(message.server.channels, name="circlejerk")
                await client.send_message(channel,"Hey, just wanted to tell you that, "+message.author.mention+" Says that he is Fluent in "+arguments[0].lower().capitalize())
                await client.send_message(message.channel, "This language is not on the list yet.\nI will ask the moderators to add it! It will be added soon (if they stop being lazy)\n\nIf you've made a mistake, type `/fluent` to see how to use the command.")

    if message.content.startswith('/whostudies') or message.content.startswith('/whostudy'):
        arguments = (message.content.split(' ')[1:])

        if len(arguments) == 0:
            await client.send_message(message.channel, "How to use :\n\t/whostudies [language]\n\nExample:\n\t/whostudies english")
        else:
            #verify if there are roles for the argument languages
            role = discord.utils.get(message.server.roles, name="Studying "+arguments[0].lower().capitalize())
            if role != None:
                students = []
                for member_i in message.server.members:
                    for role_i in member_i.roles:
                        if role_i.id == role.id:
                            students.append(member_i.name)
                if(len(students) == 0):
                    await client.send_message(message.channel, "No one is studying {}".format(arguments[0]))
                else:            
                    await client.send_message(message.channel, msg_formating(students))
            else:
                await client.send_message(message.channel, "No one is studying {}".format(arguments[0]))
    if message.content.startswith('/whonative'):
        arguments = (message.content.split(' ')[1:])

        if len(arguments) == 0:
            await client.send_message(message.channel, "How to use :\n\t/whonative [language]\n\nExample:\n\t/whonative english")
        else:
            #verify if there are roles for the argument languages
            role = discord.utils.get(message.server.roles, name=arguments[0].lower().capitalize()+" native")
            if role != None:
                natives = []
                for member_i in message.server.members:
                    for role_i in member_i.roles:
                        if role_i.id == role.id:
                            natives.append(member_i.name)              
                await client.send_message(message.channel, msg_formating(natives))
            else:
                await client.send_message(message.channel, "No one is native in {}".format(arguments[0]))
    if message.content.startswith('/whofluent'):
        arguments = (message.content.split(' ')[1:])

        if len(arguments) == 0:
            await client.send_message(message.channel, "How to use :\n\t/whofluent [language]\n\nExample:\n\t/whofluent english")
        else:
            #verify if there are roles for the argument languages
            role = discord.utils.get(message.server.roles, name="Fluent in "+arguments[0].lower().capitalize())
            if role != None:
                people = []
                for member_i in message.server.members:
                    for role_i in member_i.roles:
                        if role_i.id == role.id:
                            people.append(member_i.name)              
                await client.send_message(message.channel, msg_formating(people))
            else:
                await client.send_message(message.channel, "No one is native in {}".format(arguments[0]))
def languages_list(server):
    roles = server.roles
    languages = sorted([r.name[:-7] for r in roles if r.name[-7:] == " native"])
    longest_word = max(len(word) for word in languages)

    msg = '```'
    for item in languages:
        msg = msg + '{0:{width}}'.format(item, width=longest_word+2)
    msg = msg + '```'

    return msg
def msg_formating(item_list):
    sorted_list = sorted(item_list)
    longest_word = max(len(word) for word in sorted_list)

    msg = '```Count: ' + str(len(sorted_list)) + '\n'
    for item in sorted_list:
        msg = msg + '{0:{width}}'.format(item, width=longest_word+2)
    msg = msg + '```'

    return msg


client.run('MTc4NTk2NTYyNTA5ODg5NTM2.Cg_agg.Io49KBemgI1dZK8IgNe7xd4kB5k')