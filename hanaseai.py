import discord
import os

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        print('Message from {0.author}: {0.content}'.format(message))

        if message.content == '!ping':
            await message.channel.send('pong')

        if message.content == '!join':
            await message.author.voice.channel.connect()    
        
        if message.content == '!leave':
            await message.guild.voice_client.disconnect()
            
            

token = os.environ['TOKEN']
print(token)

client = MyClient(intents=discord.Intents.all())
client.run(str(token))