from TelegramBot.helpers.functions import get_readable_bytes
from TelegramBot.helpers.decorators import sudo_commands
from TelegramBot.logging import LOGGER
from pyrogram import Client, filters
from TelegramBot.config import *
from speedtest import Speedtest
from TelegramBot import loop

def speedtestcli():
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    return result 

commands = ["speedtest", f"speedtest@{BOT_USERNAME}"]
@Client.on_message(filters.command(commands, **prefixes))
@sudo_commands
async def speedtest(_, message: Message):
    """
    Give speedtest of server where bot is running
    """
    speed = await message.reply("Running speedtest....", quote=True)
    LOGGER(__name__).info("Running speedtest....")
    result = await loop.run_in_executor(None, speedtestcli)
	
    photo = result["share"]
    speed_string = f"""
× Upload: {get_readable_bytes(result["upload"] / 8)}/s
× Download: {get_readable_bytes(result["download"] / 8)}/s
× Ping: {result["ping"]} ms
× ISP: {result["client"]["isp"]}
"""
    await speed.delete()
    await message.reply_photo(photo=photo, caption=speed_string, quote=True)
