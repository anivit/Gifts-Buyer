from pyrogram import Client

import config


async def notifications(app: Client, star_gift_id: int, gift_price: float = None,
                        user_id: int = None, username: str = None, balance_error: bool = False,
                        error_message: str = None, non_limited_error: bool = False,
                        USAGE_LIMITED: bool = False) -> None:
    num = config.NUM_GIFTS

    if error_message:
        message = f"<b>❗Error while buying a gift!</b>\n\n" \
                  f"<pre>{error_message}</pre>"

    elif balance_error:
        message = f"<b>🎁 Gift</b> [<code>{star_gift_id}</code>] could not be sent due to insufficient balance!\n" \
                  f"<b>Please top up your balance to continue sending gifts.</b>"

    elif USAGE_LIMITED:
        message = f"<b>❗Limited gift</b> [<code>{star_gift_id}</code>] Out of Stock."

    elif non_limited_error:
        message = f"<b>❗Gift</b> [<code>{star_gift_id}</code>] is non-limited. Skipping due to user settings..."

    elif gift_price:
        message = f"<b>🎁 Gift</b> [<code>{star_gift_id}</code>] is too expensive: <b>{gift_price} ⭐</b>. Skipping..."

    else:
        message = f"<b>🎁 {f'{num} ' if num > 1 else ''}Gift{'s' if num > 1 else ''}</b> " \
                  f"[<code>{star_gift_id}</code>] has been successfully sent!\n\n" \
                  f"<b>Recipient:</b> "

        if username:
            message += f"@{username} | <code>{user_id}</code>"
        else:
            message += f'<a href="tg://user?id={user_id}">{user_id}</a>'

    try:
        await app.send_message(config.CHANNEL_ID, message.strip())
    except Exception as ex:
        print(f"\n\033[91m[ ERROR ]\033[0m Unexpected error when sending to channel: {str(ex)}")
