import os
import discord
import time
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from db import add_job,last_job_time
from worker import job_queue, worker, Job
from worker import worker

RATE_LIMIT = 300 # 5 minutes

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    bot.loop.create_task(worker())
    print(f"Logged in as {bot.user}")
    print("Worker started")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == "Hi" or "hi":
        await message.channel.send("<:BCIS_Hi:emojiID>") # Found by running "\:emojiname:" in Discord

    await bot.process_commands(message)

@bot.command()
async def crack(ctx, hash_value: str):
    user_id = str(ctx.author.id)

    last = last_job_time(user_id)

    if last and time.time() - last < RATE_LIMIT:
        remaining = int(RATE_LIMIT - (time.time() - last))
        await ctx.send(f"Rate limit active. Try again in {remaining}s.")
        return

    add_job(user_id, hash_value)
    job = Job(ctx, hash_value)
    await job_queue.put(job)
    await ctx.send("Hash queued successfully.")

bot.run(TOKEN)