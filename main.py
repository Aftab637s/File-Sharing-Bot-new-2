import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

from bot import Bot

Bot().run()
