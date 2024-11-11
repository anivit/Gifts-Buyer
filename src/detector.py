# ========================
# Made with ❤️ by @B7XX7B
# ========================

import asyncio
import json
import time
import typing

from pyrogram import Client, types
from pytz import timezone as _timezone

import config
from src import utils

timezone = _timezone(config.TIMEZONE)


async def detector(app: Client, new_callback: typing.Callable, update_callback: typing.Callable,
                   connect_every_loop: bool = True) -> None:
    dot_counter = 0
    while True:
        current_time = utils.current_datetime(timezone)
        dot_counter += 1
        dots = '.' * dot_counter
        print(f"\033[K\033[94m[ INFO ]\033[0m {current_time} \033[1m- Checking for new gifts{dots}\033[0m", end="\r")

        if dot_counter >= 3:
            dot_counter = 0

        time.sleep(0.2)

        if not app.is_connected:
            await app.start()

        old_star_gifts_raw: list[dict]

        try:
            with config.DATA_FILEPATH.open("r", encoding='utf-8') as file:
                old_star_gifts_raw = json.load(file)
        except FileNotFoundError:
            old_star_gifts_raw = []

        old_star_gifts_raw_dict = {gift["id"]: gift for gift in old_star_gifts_raw}

        all_star_gifts_raw = [
            json.loads(json.dumps(gift, indent=4, default=types.Object.default, ensure_ascii=False))
            for gift in await app.get_star_gifts()
        ]

        all_star_gifts_raw_dict = {gift["id"]: gift for gift in all_star_gifts_raw}

        new_star_gifts_raw = {
            key: value for key, value in all_star_gifts_raw_dict.items() if key not in old_star_gifts_raw_dict
        }

        all_star_gifts_ids = list(all_star_gifts_raw_dict.keys())
        all_star_gifts_amount = len(all_star_gifts_ids)

        if new_star_gifts_raw:
            print(f"\n\n\033[92m[ NEW ]\033[0m New gifts found: {len(new_star_gifts_raw)}")

            for star_gift_id, star_gift_raw in new_star_gifts_raw.items():
                star_gift_raw["number"] = all_star_gifts_amount - all_star_gifts_ids.index(star_gift_id)

            for star_gift_id, star_gift_raw in sorted(new_star_gifts_raw.items(), key=lambda it: it[1]["number"]):
                await new_callback(app, star_gift_raw)

        with config.DATA_FILEPATH.open("w", encoding='utf-8') as file:
            json.dump(all_star_gifts_raw, file, indent=4, default=types.Object.default, ensure_ascii=False)

        if connect_every_loop:
            await app.stop()

        await asyncio.sleep(config.INTERVAL)
