import discord
from discord.ext import tasks
import datetime
import pytz
import os

BOT_TOKEN = os.environ["TOKEN"]
DISCORD_CHANNEL_ID = 1520127730178326619
WELCOME_CHANNEL_ID = 1521127085362380901

MEMBERS = [
    {"name": "서연", "month": 8, "day": 6},
    {"name": "혜린", "month": 4, "day": 12},
    {"name": "지우", "month": 10, "day": 24},
    {"name": "채연", "month": 12, "day": 4},
    {"name": "유연", "month": 2, "day": 9},
    {"name": "수민", "month": 10, "day": 3},
    {"name": "나경", "month": 10, "day": 13},
    {"name": "유빈", "month": 2, "day": 3},
    {"name": "에데", "month": 12, "day": 20},
    {"name": "다현", "month": 1, "day": 8},
    {"name": "토네", "month": 3, "day": 10},
    {"name": "연지", "month": 1, "day": 8},
    {"name": "니엔", "month": 6, "day": 2},
    {"name": "소현", "month": 10, "day": 13},
    {"name": "신위", "month": 5, "day": 25},
    {"name": "마유", "month": 5, "day": 12},
    {"name": "린", "month": 4, "day": 12},
    {"name": "주빈", "month": 1, "day": 16},
    {"name": "하연", "month": 8, "day": 1},
    {"name": "시온", "month": 4, "day": 3},
    {"name": "채원", "month": 5, "day": 2},
    {"name": "설린", "month": 11, "day": 30},
    {"name": "서아", "month": 6, "day": 11},
    {"name": "지연", "month": 2, "day": 13},
]

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@tasks.loop(minutes=1)
async def check_birthday():
    kst = pytz.timezone("Asia/Seoul")
    now = datetime.datetime.now(kst)

    if now.hour != 0 or now.minute != 0:
        return

    channel = client.get_channel(DISCORD_CHANNEL_ID)
    if not channel:
        return

    for member in MEMBERS:
        if member["month"] == now.month and member["day"] == now.day:
            await channel.send(f"오늘은 **{member['name']}이**의 생일이에요!")

@client.event
async def on_member_join(member):
    channel = client.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        return

    embed = discord.Embed(
        description=f"환영해요, {member.mention}!\n왹왹서버에 오신 것을 환영합니다 🎉",
        color=0xf8a4c8
    )

    if member.banner:
        embed.set_image(url=member.banner.url)

    await channel.send(embed=embed)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        return

    await channel.send(f"{member.mention}님이 서버를 떠났어요 👋")

@client.event
async def on_ready():
    print(f"✅ {client.user} 시작됨!")
    check_birthday.start()

client.run(BOT_TOKEN)
