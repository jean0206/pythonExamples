import discord

class myClient(discord.Client):
    async def on_ready(self):
        print(self.user)

    async def on_message(self,message):
        print(message)

client= myClient()
client.run("ODAwMjgxMzE1MDEzNDI3MjMw.YAP2Dg.WSOywjdklre2QgvLp4LK8UCzriA")
