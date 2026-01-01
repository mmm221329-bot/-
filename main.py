import discord
from discord.ext import commands
import requests
import asyncio
import random
import string
import os
from flask import Flask
from threading import Thread

# --- إعداد السيرفر لضمان البقاء حياً على Render ---
app = Flask('')

@app.route('/')
def home():
    return "✅ Radar is Live and Running"

def run():
    # سحب البورت من إعدادات Render تلقائياً لفتح المنفذ
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات البوت بالتوكن الجديد ---
TOKEN = 'MTQ1NTI5NDUyMDM3NDg1Nzg2Ng.G9s1Xq.hDbQK7sxvMVohbUnWsaIaQBiGsx4u8DTcAs8vE'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

hunting = False

@bot.event
async def on_ready():
    print(f"✅ تم الاتصال بنجاح باسم: {bot.user}")

@bot.command()
async def check(ctx, length: int = 4):
    global hunting
    if hunting:
        return await ctx.send("⚠️ الرادار يعمل بالفعل!")
    
    hunting = True
    await ctx.send(f"🛰️ **بدأ الرادار... جاري فحص يوزرات طول {length}**")

    while hunting:
        target = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        try:
            res = requests.get(f"https://www.instagram.com/{target}/", timeout=5)
            if res.status_code == 404:
                await ctx.send(f"🎯 **صيدة متاح:** `@{target}`")
            await asyncio.sleep(1.2) # تأخير بسيط لتجنب الحظر
        except:
            await asyncio.sleep(5)

@bot.command()
async def stop(ctx):
    global hunting
    hunting = False
    await ctx.send("🛑 تم إيقاف الرادار.")

if __name__ == "__main__":
    keep_alive() # تشغيل ميزة الـ Keep Alive
    bot.run(TOKEN)
