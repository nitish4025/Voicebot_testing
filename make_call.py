"""
Voicebot - Make outbound calls using Twilio.

Uses inline TwiML so no callback server is needed.

Usage:
    python make_call.py --target +1XXXXXXXXXX
    python make_call.py  (uses TARGET_PHONE_NUMBER from .env)
"""

import argparse
import os
import sys
import time

from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

load_dotenv()


def get_client():
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    phone_number = os.getenv("TWILIO_PHONE_NUMBER")

    if not account_sid:
        sys.exit("Error: TWILIO_ACCOUNT_SID not set. See .env.example")
    if not auth_token:
        sys.exit("Error: TWILIO_AUTH_TOKEN not set. See .env.example")
    if not phone_number:
        sys.exit("Error: TWILIO_PHONE_NUMBER not set. See .env.example")

    return Client(account_sid, auth_token), phone_number


def make_call(target_number: str, message: str = None):
    client, source_number = get_client()

    # Build TwiML inline — no callback server needed
    response = VoiceResponse()
    response.say(
        message or "Hello! This is an automated call from the voicebot. Have a great day!",
        voice="Polly.Joanna",
        language="en-US",
    )
    response.pause(length=1)
    response.say("Goodbye!", voice="Polly.Joanna")

    twiml_str = str(response)
    print(f"Calling {target_number} from {source_number}...")

    call = client.calls.create(
        to=target_number,
        from_=source_number,
        twiml=twiml_str,
    )

    print(f"Call initiated! SID: {call.sid}")

    # Poll for call status
    while call.status not in ("completed", "failed", "busy", "no-answer", "canceled"):
        time.sleep(3)
        call = call.fetch()
        print(f"  Status: {call.status}")

    print(f"Final status: {call.status} | Duration: {call.duration}s")
    return call


def main():
    parser = argparse.ArgumentParser(description="Make an outbound call via Twilio")
    parser.add_argument(
        "--target",
        type=str,
        default=os.getenv("TARGET_PHONE_NUMBER"),
        help="Target phone number in E.164 format (e.g., +14155551234)",
    )
    parser.add_argument(
        "--message",
        type=str,
        default=None,
        help="Custom message to speak during the call",
    )
    args = parser.parse_args()

    if not args.target:
        sys.exit("Error: Provide --target or set TARGET_PHONE_NUMBER in .env")

    make_call(args.target, args.message)


if __name__ == "__main__":
    main()
