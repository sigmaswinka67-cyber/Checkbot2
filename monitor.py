import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
from database import add_incident

URL = "https://checkbot-production-b44c.up.railway.app/"

bots_data = {}
monitor_enabled = True


async def fetch_status():

    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")

    rows = soup.find_all("tr")[1:]

    bots = []

    for row in rows:

        cols = row.find_all("td")

        name = cols[0].text.strip()
        status = cols[1].text.strip()
        last_seen = cols[2].text.strip()

        bots.append((name, status, last_seen))

    return bots


async def monitor_loop(fetch_func, alert_func):

    global monitor_enabled

    while True:

        if not monitor_enabled:
            await asyncio.sleep(5)
            continue

        bots = await fetch_func()

        for name, status, last_seen in bots:

            try:
                last_seen_time = datetime.fromisoformat(last_seen)

                diff = (datetime.utcnow() - last_seen_time).total_seconds()

                if diff > 60:

                    if bots_data.get(name) != "OFFLINE":

                        bots_data[name] = "OFFLINE"

                        add_incident(name)

                        await alert_func(name)

                else:

                    bots_data[name] = "ONLINE"

            except:
                bots_data[name] = "UNKNOWN"

        await asyncio.sleep(30)