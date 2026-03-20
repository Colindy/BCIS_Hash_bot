import asyncio
import subprocess
import queue

job_queue = asyncio.Queue()

class Job:
    def __init__(self, ctx, hash_value):
        self.ctx = ctx
        self.hash = hash_value

async def worker():
    while True:
        job = await job_queue.get()

        await job.ctx.send("🔧 Running hashcat...")

        # run cracking job
        process = await asyncio.create_subprocess_exec(
            "hashcat",
            "-m", "0",
            job.hash,
            "-a", "0",
            "/usr/share/wordlists/SecLists/Passwords/Leaked-Databases/rockyou.txt",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        await process.communicate()

        # check result using --show
        show = await asyncio.create_subprocess_exec(
            "hashcat",
            "-m", "0",
            "--show",
            job.hash,
            stdout=asyncio.subprocess.PIPE
        )

        stdout, _ = await show.communicate()
        result = stdout.decode().strip()

        if result:
            plaintext = result.split(":")[1]
            await job.ctx.send(f"✅ Cracked: `{plaintext}`")
        else:
            await job.ctx.send("❌ Hash not cracked.")

        job_queue.task_done()