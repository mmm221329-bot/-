import discord
from discord.ext import commands
import requests
import asyncio
import random
import string
import os
from flask import Flask
from threading import Thread

# --- إعداد السيرفر للبقاء حياً ---
app = Flask('')
@app.route('/')
def home(): return "✅ Radar is Secure and Live"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- سحب التوكن بأمان من إعدادات الريندر ---
TOKEN = os.environ.get('TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

hunting = False

@bot.event
async def on_ready():
    print(f"✅ تم الاتصال بأمان باسم: {bot.user}")

@bot.command()
async def check(ctx, length: int = 4):
    global hunting
    if hunting: return await ctx.send("⚠️ الرادار يعمل!")
    hunting = True
    await ctx.send(f"🛰️ جاري الفحص...")
    while hunting:
        target = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        try:
            res = requests.get(f"https://www.instagram.com/{target}/", timeout=5)
            if res.status_code == 404:
                await ctx.send(f"🎯 متاح: `@{target}`")
            await asyncio.sleep(1.2)
        except: await asyncio.sleep(5)

if __name__ == "__main__":
    keep_alive()
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ خطأ: لم يتم العثور على التوكن في Environment Variables")
