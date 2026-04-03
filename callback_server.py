"""
Callback server to handle Twilio call events.

When Twilio connects a call, it requests TwiML instructions from your server.
This server tells Twilio what to say, play, or do during the call.

Usage:
    python callback_server.py
    (Then expose port 5000 via ngrok: ngrok http 5000)
"""

from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)


@app.route("/voice", methods=["POST"])
def voice():
    """Called when the target answers. Return TwiML instructions."""
    print(f"Call answered! From: {request.form.get('From')} To: {request.form.get('To')}")

    response = VoiceResponse()
    response.say(
        "Hello! This is an automated call from the voicebot. How can I help you today?",
        voice="Polly.Joanna",
        language="en-US",
    )
    response.pause(length=2)
    response.say("Goodbye!", voice="Polly.Joanna")
    response.hangup()

    return str(response), 200, {"Content-Type": "text/xml"}


@app.route("/status", methods=["POST"])
def status():
    """Receive call status updates."""
    call_sid = request.form.get("CallSid")
    call_status = request.form.get("CallStatus")
    print(f"Call {call_sid}: {call_status}")
    return "", 204


@app.route("/health", methods=["GET"])
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    print("Starting callback server on port 5000...")
    print("Expose this with: ngrok http 5000")
    app.run(port=5000, debug=True)
