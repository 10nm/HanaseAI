import discord
import openai
import os

openai.api_key = "EMPTY"
openai.base_url = "http://localhost:8000/v1/"
model = "vicuna-7b-v1.5"

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
 
    async def on_message(self, message):
        ct = message.content

        if message.author == self.user:
            return
        
        print('Message from {0.author}: {0.content}'.format(message))

        if message.content == '!ping':
            await message.channel.send('pong')

        if message.content == '!join':
            await message.author.voice.channel.connect()    
        
        if message.content == '!leave':
            await message.guild.voice_client.disconnect()
        
        if ct.startswith('.') == True:
            prompt = (message.content)
            prompt = prompt.lstrip('.')
            completion = await nlp(prompt)
            await message.channel.send(completion.choices[0].text)

async def nlp(prompt):
    response= openai.completions.create(
        model=model, 
        prompt=prompt, 
        max_tokens=64,
    )
    return response

token = os.environ.get("TOKEN")
print(token)

client = MyClient(intents=discord.Intents.all())
client.run(str(token))