import asyncio

from bot.core import dp, bot, sheduler
from bot.ap_shedule import send_message_interval


async def main():
    sheduler.add_job(send_message_interval, "interval", seconds=10, args=(bot,))

    try:
        # sheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        pass
