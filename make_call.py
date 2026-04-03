"""
Voicebot - Make outbound calls using Azure Communication Services.

Usage:
    python make_call.py --target +1XXXXXXXXXX
    python make_call.py  (uses TARGET_PHONE_NUMBER from .env)
"""

import argparse
import os
import sys

from dotenv import load_dotenv
from azure.communication.callautomation import (
    CallAutomationClient,
    PhoneNumberIdentifier,
)

load_dotenv()


def get_config():
    connection_string = os.getenv("ACS_CONNECTION_STRING")
    phone_number = os.getenv("ACS_PHONE_NUMBER")
    callback_uri = os.getenv("CALLBACK_URI")

    if not connection_string:
        sys.exit("Error: ACS_CONNECTION_STRING not set. See .env.example")
    if not phone_number:
        sys.exit("Error: ACS_PHONE_NUMBER not set. See .env.example")
    if not callback_uri:
        sys.exit("Error: CALLBACK_URI not set. See .env.example")

    return connection_string, phone_number, callback_uri


def make_call(target_number: str):
    connection_string, source_number, callback_uri = get_config()

    client = CallAutomationClient.from_connection_string(connection_string)

    target = PhoneNumberIdentifier(target_number)
    source = PhoneNumberIdentifier(source_number)

    print(f"Calling {target_number} from {source_number}...")

    call_result = client.create_call(
        target_participant=target,
        source_caller_id_number=source,
        callback_url=f"{callback_uri}/api/callbacks",
    )

    print(f"Call initiated successfully!")
    print(f"Call connection ID: {call_result.call_connection_id}")
    return call_result


def main():
    parser = argparse.ArgumentParser(description="Make an outbound call via Azure Communication Services")
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
