import discord
from discord.interactions import Interaction
import requests
import random
import json
import os
from discord.ui import Button, View
from discord import app_commands,ui

intents = discord.Intents.all()
client = discord.Client(intents=intents)

MYGUILD = discord.Object(id=1114949386619850762) # uid เซิฟเวอร์ของคุณ

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

def call_api(username, password, tmemail, action, transactionid, clientip, ref1, json_one):
    base_url = "https://www.tmweasy.com/apiwallet.php"

    url = f"{base_url}?username={username}&password={password}&tmemail={tmemail}&action={action}&transactionid={transactionid}&clientip={clientip}&ref1={ref1}&json={json_one}"

    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        return None


def generate_random_number():
    num1 = random.randint(100, 999)
    num2 = random.randint(100, 999)
    num3 = random.randint(100, 999)
    num4 = random.randint(10, 99)
    return f"{num1}.{num2}.{num3}.{num4}"


class shopping_discord(discord.ui.Modal, title="เติมเงิน"):
    link_angpao = discord.ui.TextInput(label="Link", placeholder="ใส่ลิ้งอังเปาของคุณ", required=True, max_length=100, style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        random_number = generate_random_number()
        with open('API_Wallet_User_Nane.json') as json_user_pass:
            data_user_pass = json.load(json_user_pass)
        username_tMWeasy = data_user_pass['username']
        password_tMWeasy = data_user_pass['password']
        uid = str(interaction.user.id)
        name_user = interaction.user.name
        username = username_tMWeasy # กรอก username ในไฟล์ API_Wallet_User_Nane.json ที่สมัครสมาชิกไว้ เว็ป tmweasy
        password = password_tMWeasy # กรอก password ในไฟล์ API_Wallet_User_Nane.json ที่สมัครสมาชิกไว้ เว็ป tmweasy
        tmemail = "" # กรอกเบอร์ตรงนี้
        action = "yes"
        transactionid = self.link_angpao
        clientip = f"{random_number}"
        ref1 = username_tMWeasy 
        json_one = "1"
        response = call_api(username, password, tmemail, action, transactionid, clientip, ref1, json_one)
        if response is not None:
            status = response.get('Status')
            money = response.get('Amount')
            # เวลาคนเติมเงิน จะบันทึกสร้างไฟล์ uid.json เก็บข้อมูลเงินที่รับมาไว้ในไฟล์
            if status == 'check_success':
                data = {
                    f"{uid}": {
                        "money": money,
                        "name": name_user
                        }
                    }
                folder_name = "money_id"
                file_name = f"{uid}.json"
                file_path = os.path.join(folder_name, file_name)
                os.makedirs(folder_name, exist_ok=True)  
                with open(file_path, 'w') as file_money:
                    json.dump(data, file_money, indent=4)
                embed = discord.Embed(title="\nทำรายการสำเร็จ", description=f"**เติมเงินสำเร็จเเล้ว จำนวน {money} บาท**", color=0xB0FC38)
                await interaction.response.send_message(embed=embed, delete_after=30)
            elif status == 'check_failed':
                embed = discord.Embed(title="\nทำรายการไม่สำเร็จ", description=f"**ขออภัยเติมเงินไม่สำเร็จหรือลิ้งอังเปาไม่ถูกต้อง !**", color=0xFF0000)
                await interaction.response.send_message(embed=embed, delete_after=30)
            else:
                # ถ้าบอทเเจ้งเตือนเเบบนี้ เราต้องเติมเครดิตจากเว็ป tmweasy ก่อน สมัครครั้งเเรกได้รับฟรี 5 เครดิตจากทางเว็ป
                embed = discord.Embed(title="\nเกิดข้อผิดพลาด", description=f"**ขออภัยระบบอังเปาเกิดข้อผิดพลาดในระบบโปรดเก็บซองของคุณไว้ให้ดี !**", color=0xFF0000)
                await interaction.response.send_message(embed=embed, delete_after=30)
        else:
            print("Request failed.")      


@client.tree.command(description="เติมเงินด้วยอั่งเปาทรูมันนี่วอลเล็ท")
async def fill_money(interaction: discord.Interaction):
    guild_server = interaction.guild.icon.url
    username = interaction.user.name
    server_name = interaction.guild.name
    button = Button(label="เติมเงิน", style=discord.ButtonStyle.green, emoji="🧧")
    async def button_callback(interaction: discord.Interaction):
        await interaction.response.send_modal(shopping_discord())
    button.callback = button_callback
    view = View()
    view.add_item(button)

    embed = discord.Embed(title="\nระบบเติมเงิน", description=f"**WELCOME TO SERVER !**\n\n**• {server_name}**", color=0xFCE5CD)
    embed.set_author(name=username, icon_url=guild_server, url="https://discord.com/channels/@me/"+username)
    # ด้านล่างนี้เเก้ตกเเต่งได้ตามใจชอบเลย !
    embed.add_field(name="- 📄 __EXAMPLE ( ตัวอย่าง )__", value="เติมเงินได้ขั้นต่ํา 10 บาทขึ้นไปเพียงใส่ลิ้งซองอังเปาระบบก็ทำการเติมเงินให้คุณเเล้ว\nเติมเเล้วขอเงินคืนเเอดมินจะไม่คืนเงินใดๆทั้งสิ้นเช็คยอดเงินตัวเอง\nคำสั้ง ||__/check_money__||",inline=False)
    embed.add_field(name="- 📢 __PROMOTION ( โปรโมชั่นพิเศษ )__", value="เติมเงิน 100 บาทขึ้นไปได้ยศ VIP ปลดล็อคห้องเเจกสคริปส์ต่างๆ,ใช้งานห้องบอทต่างๆได้ฟรี!", inline=False)
    embed.add_field(name="- 🧧 __CREATEANGPAO ( สร้างซองอังเปา )__", value="Link Youtube - ||https://youtu.be/kgEotqNRzrc||")
    embed.set_thumbnail(url="https://www.truemoney.com/wp-content/uploads/2022/01/truemoneywallet-sendgift-hongbao-20220125-icon-2.png")
    embed.set_image(url="https://i.gifer.com/EKpo.gif")
    await interaction.response.send_message(embed=embed, view=view, delete_after=120)




@client.tree.command(description="เช็คจำนวนเงินของคุณ")
async def check_money(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    folder_name = "money_id"
    file_name = f"{uid}.json"
    file_path = os.path.join(folder_name, file_name)

    try:
        with open(file_path, 'r') as file_money:
            data = json.load(file_money)
        money = data[uid]["money"]
        embed = discord.Embed(title="\nเช็คยอดเงินของคุณ", description=f"**จำนวนเงินในระบบของคุณมีอยู่ {money} บาท**", color=0xFCE5CD)
        await interaction.response.send_message(embed=embed, delete_after=30)
    except FileNotFoundError:
        embed = discord.Embed(title="\nเกิดข้อผิดพลาด", description=f"**ไม่ได้เติมเงินในระบบโปรดเติมเงินก่อน !**", color=0xFF0000)
        await interaction.response.send_message(embed=embed, delete_after=30)

client.run('') # กรอก token bot ของคุณ