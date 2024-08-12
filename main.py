from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
import json

import rss_feed
import email_reader

app = FastAPI()

with open("login_data.json", "r") as f:
    login_data = json.load(f)

with open("settings.json", "r") as f:
    settings = json.load(f)

TOKEN = settings["TOKEN"]

@app.get("/{email}")
async def email_to_rss(email: str, token: str, request: Request, reverse: bool = False):
    # Validate token
    if token != TOKEN: return Response(content="Unauthorized!", status_code=401)

    # Check login info
    if email not in login_data: return Response(content="Login info is missing!", status_code=401)
    if "server" not in login_data[email] or "password" not in login_data[email]: return Response(content="Login info is missing!", status_code=401)

    emails = email_reader.get_emails(email, login_data[email]["password"], login_data[email]["server"]) # fetch the emails
    rss = rss_feed.generate_rss(email, emails, reverse)                                                 # generate an RSS feed
    return Response(content=rss, media_type="application/xml")                                          # return the RSS feed