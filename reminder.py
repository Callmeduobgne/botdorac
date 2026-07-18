import asyncio
import html
import json
import os
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from telegram import Bot


TIMEZONE = ZoneInfo("Asia/Ho_Chi_Minh")
START_DATE = date(2026, 7, 18)
MEMBERS_FILE = Path(__file__).with_name("members.json")


def load_members() -> list[dict]:
    with MEMBERS_FILE.open("r", encoding="utf-8") as file:
        members = json.load(file)

    if not members:
        raise ValueError("members.json must contain at least one member")

    return members


def member_for_day(members: list[dict], today: date) -> dict:
    days_since_start = (today - START_DATE).days

    if days_since_start < 0:
        raise ValueError(
            f"The rotation has not started yet (start date: {START_DATE:%d/%m/%Y})"
        )

    return members[days_since_start % len(members)]


async def main() -> None:
    today = datetime.now(TIMEZONE).date()

    if today < START_DATE:
        print(f"Rotation starts on {START_DATE:%d/%m/%Y}; no reminder sent.")
        return

    bot_token = os.environ["BOT_TOKEN"]
    group_id = int(os.environ["GROUP_ID"])
    person = member_for_day(load_members(), today)

    name = html.escape(str(person["name"]))
    message = (
        "🗑️ <b>NHẮC ĐỔ RÁC</b>\n\n"
        f"👉 {name} nay đổ rác, lồng túi rác."
    )

    async with Bot(token=bot_token) as bot:
        await bot.send_message(
            chat_id=group_id,
            text=message,
            parse_mode="HTML",
        )


if __name__ == "__main__":
    asyncio.run(main())
