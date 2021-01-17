import discord

class myClient(discord.Client):
    async def on_ready(self):
        print(self.user)

    async def on_message(self,message):
        print(message)

client= myClient()
client.run("")
