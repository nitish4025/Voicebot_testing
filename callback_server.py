"""
Callback server to handle Azure Communication Services call events.

Azure sends webhook events during a call (connected, disconnected, DTMF tones, etc.).
This server handles those events and can play audio, recognize speech, or hang up.

Usage:
    python callback_server.py
    (Then expose port 5000 via ngrok: ngrok http 5000)
"""

import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from azure.communication.callautomation import (
    CallAutomationClient,
    CallAutomationEventParser,
    TextSource,
)

load_dotenv()

app = Flask(__name__)

connection_string = os.getenv("ACS_CONNECTION_STRING")
client = CallAutomationClient.from_connection_string(connection_string)


@app.route("/api/callbacks", methods=["POST"])
def callbacks():
    """Handle call automation events from Azure."""
    for event_dict in request.json:
        event = CallAutomationEventParser.parse(event_dict)
        call_connection_id = event.call_connection_id

        event_type = type(event).__name__
        print(f"Event received: {event_type} (connection: {call_connection_id})")

        if event_type == "CallConnected":
            handle_call_connected(call_connection_id)
        elif event_type == "PlayCompleted":
            handle_play_completed(call_connection_id)
        elif event_type == "CallDisconnected":
            print("Call ended.")

    return jsonify({"status": "ok"}), 200


def handle_call_connected(call_connection_id: str):
    """Called when the target answers. Play a greeting message."""
    print("Call connected! Playing greeting...")

    call_connection = client.get_call_connection(call_connection_id)
    greeting = TextSource(
        text="Hello! This is an automated call from the voicebot. How can I help you today?",
        voice_name="en-US-JennyNeural",
    )
    call_connection.play_media_to_all(greeting)


def handle_play_completed(call_connection_id: str):
    """Called when audio playback finishes."""
    print("Playback completed. Hanging up.")
    call_connection = client.get_call_connection(call_connection_id)
    call_connection.hang_up(is_for_everyone=True)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    print("Starting callback server on port 5000...")
    print("Expose this with: ngrok http 5000")
    app.run(port=5000, debug=True)
