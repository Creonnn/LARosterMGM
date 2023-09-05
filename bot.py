# from image_to_text import *
from dotenv import load_dotenv
import discord, os, messages, roster


def run_discord_bot():
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print("We have logged in as {0.user}".format(client))
    
    @client.event
    async def on_message(message):
        disc_id = str(message.author.id)
        user_message = str(message.content)
        svr_id = str(message.guild.id)

        if message.author == client.user:
            return

        if user_message == "$help":
            await message.channel.send(f"```{messages.help}```")

        elif user_message == "$help add":
            await message.channel.send(f"```{messages.help_add}```")

        elif user_message == "$help roster":
            await message.channel.send(f"```{messages.help_roster}```")

        elif user_message == "$help statistics":
            await message.channel.send(f"```{messages.help_statistics}```")

        elif user_message == "$help overview":
            await message.channel.send(f"```{messages.help_overview}```")

        elif user_message == "$help update":
            await message.channel.send(f"```{messages.help_update}```")

        elif user_message == "$help delete":
            await message.channel.send(f"```{messages.help_delete}```")

        elif user_message[:4] == "$add" or (user_message[:2] == "$a" and user_message[:4] != "$aui"):
            '''
            Adds a character to user's roster
            '''
            msg = user_message[5:] if user_message[:4] == "$add" else user_message[3:]

            if not roster.valid_add_inputs(msg):
                await message.channel.send('One or more of your inputs are incorrect. If you need help, type **$help add** for proper formatting.')

            elif roster.add(msg, svr_id, disc_id):
                await message.channel.send('Successfully added')

            else:
                await message.channel.send('Cannot add due to duplicate entry')

        elif user_message[0:7] == "$roster" or (user_message[:2] == "$r" and user_message != '$rankings'):
            '''
            If user just types $roster, this will display their own roster stored within database

            If user types $roster @<username>, this will display that discord user's roster stores within database
            '''
            msg = user_message[8:] if user_message[0:7] == "$roster" else user_message[3:]
            if roster.display_roster(disc_id, svr_id, msg) == '':
                await message.channel.send("```No information found for that user```")

            else:
                await message.channel.send(f"```{roster.display_roster(disc_id, svr_id, msg)}```")

        elif user_message == "$statistics":
            #Todo: Displays general statistics for overall roster of everyone (average ilvl, class distributions, ilvl distribution, ...)
            img1, img2, avg_ilvl = roster.statistics(svr_id)
            await message.channel.send(f'{img1}')
            await message.channel.send(f'{img2}')
            await message.channel.send(f'```Average ilvl: {avg_ilvl}```')

        elif user_message == "$rankings":
            '''
            Diplays top 10 character ilvls
            '''
            await message.channel.send(f"```{roster.ranking(svr_id)}```")

        elif user_message == "$overview":
            '''
            Displays everyone's roster in the specified discord server
            '''
            await message.channel.send(f"```{roster.overview(svr_id)}```")

        elif user_message[:7] == "$update" or user_message[:2] == "$u":
            # allows user to modify an attribute for one of their roster characters
            msg = user_message[8:] if user_message[:7] == "$update" else user_message[3:]

            if roster.update(svr_id, disc_id, msg):
                await message.channel.send(f"```Successfully updated\n"\
                                           f"Details\n"\
                                           f"Change made for: {msg.split(',')[0].strip().title()}\n"\
                                           f"{msg.split(',')[1].strip().title()} = {msg.split(',')[2].strip().title()}```")
            else:
                await message.channel.send(f"One or more of your entries were incorrect. Type **$help update** for proper syntax")

        elif user_message[:7] == "$delete" or user_message[:2] == "$d":
            msg = user_message[8:] if user_message[:7] == "$delete" else user_message[3:]

            if roster.delete(svr_id, disc_id, msg):
                name = user_message[8:].strip().title() if user_message[:7] == "$delete" else user_message[3:].title()
                await message.channel.send(f"```Successfully deleted {name}```")

            else:
                await message.channel.send(f"One or more of your entries were incorrect. Type **$help delete** for proper syntax")
        '''
        elif user_message == "$test":
            img = message.attachments[0]
            class_name, char, ilvl = image_to_text.convert(img)
            await message.channel.send(f'Character Name: {char}, Class: {class_name}, ilvl: {ilvl}')
        '''
        #elif user_message[:4] == "$aui":
        #    img = message.attachments[0]
        #    class_name, char, ilvl = image_to_text.convert(img)
        #    print()

        #    if roster.add_using_image(char, class_name, ilvl, svr_id, disc_id):
        #        await message.channel.send('Successfully added')

        #    else:
        #        await message.channel.send('Cannot add due to duplicate entry')

        #Todo: raid scheduling

    load_dotenv()
    client.run(os.getenv('TOKEN'))
    

