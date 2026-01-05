from aiohttp import web
import asyncio

# Dummy HTTP server for Koyeb health checks
async def handle(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get("/", handle)

# Run aiohttp server in the background
async def start_webserver():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()

# Start everything
async def main():
    await start_webserver()  # start dummy HTTP server
    scheduler.start()        # start your APScheduler jobs
    print("Scheduler started. Bot is running...")

# Run the asyncio loop
asyncio.run(main())