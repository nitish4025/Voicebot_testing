"""
Voicebot - Make outbound calls using Twilio.

Usage:
    python make_call.py --target +1XXXXXXXXXX
    python make_call.py  (uses TARGET_PHONE_NUMBER from .env)
"""

import argparse
import os
import sys

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


def get_config():
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    phone_number = os.getenv("TWILIO_PHONE_NUMBER")
    callback_uri = os.getenv("CALLBACK_URI")

    if not account_sid:
        sys.exit("Error: TWILIO_ACCOUNT_SID not set. See .env.example")
    if not auth_token:
        sys.exit("Error: TWILIO_AUTH_TOKEN not set. See .env.example")
    if not phone_number:
        sys.exit("Error: TWILIO_PHONE_NUMBER not set. See .env.example")
    if not callback_uri:
        sys.exit("Error: CALLBACK_URI not set. See .env.example")

    return account_sid, auth_token, phone_number, callback_uri


def make_call(target_number: str):
    account_sid, auth_token, source_number, callback_uri = get_config()

    client = Client(account_sid, auth_token)

    print(f"Calling {target_number} from {source_number}...")

    call = client.calls.create(
        to=target_number,
        from_=source_number,
        url=f"{callback_uri}/voice",
        status_callback=f"{callback_uri}/status",
        status_callback_event=["initiated", "ringing", "answered", "completed"],
    )

    print(f"Call initiated successfully!")
    print(f"Call SID: {call.sid}")
    print(f"Status: {call.status}")
    return call


def main():
    parser = argparse.ArgumentParser(description="Make an outbound call via Twilio")
    parser.add_argument(
        "--target",
        type=str,
        default=os.getenv("TARGET_PHONE_NUMBER"),
        help="Target phone number in E.164 format (e.g., +14155551234)",
    )
    args = parser.parse_args()

    if not args.target:
        sys.exit("Error: Provide --target or set TARGET_PHONE_NUMBER in .env")

    make_call(args.target)


if __name__ == "__main__":
    main()
