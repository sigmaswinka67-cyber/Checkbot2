from fastapi import FastAPI
from monitor import bots_data
from database import get_incidents

app = FastAPI()


@app.get("/")
def dashboard():

    html = "<h1>Bot Monitor</h1><table border=1>"

    for bot, status in bots_data.items():

        color = "green" if status == "ONLINE" else "red"

        html += f"<tr><td>{bot}</td><td style='color:{color}'>{status}</td></tr>"

    html += "</table>"

    html += "<h2>История падений</h2>"

    for bot, time in get_incidents():

        html += f"<p>{bot} — {time}</p>"

    return html