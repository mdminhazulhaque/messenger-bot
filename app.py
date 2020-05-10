#!/usr/bin/env python3

from flask import Flask, request
import requests

PAGE_ACCESS_TOKEN = "ONE-HUGE-PAGE-TOKEN-TO-PUT-HERE-ONE-HUGE-PAGE-TOKEN-TO-PUT-HERE-ONE-HUGE-PAGE-TOKEN-TO-PUT-HERE-ONE-HUGE-PAGE-TOKEN-TO-PUT-HERE-ONE-HUGE-PAGE-TOKEN-TO-PUT-HERE"
VERIFY_TOKEN = "GENERATE-ANY-RANDOM-STRING"

def handle_message(msg):
    # do something with msg
    return "You said " + msg

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "OK", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"]["text"]
                    response = handle_message(message_text)
                    send_message(sender_id, response)
    return "OK", 200

@app.route('/callback', methods=['POST'])
def callback():
    response = request.get_json()["response"]
    send_message("1585364548150991", response)
    return "OK", 200

def send_message(recipient_id, response):
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": response
        }
    }
    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, json=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, ssl_context=(
        '/etc/letsencrypt/live/mdminhazulhaque.io/fullchain.pem',
        '/etc/letsencrypt/live/mdminhazulhaque.io/privkey.pem'
        )
    )
