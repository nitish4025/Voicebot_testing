# Voicebot Testing

Make outbound phone calls using Twilio.

## Setup

### 1. Configure Environment

```bash
cp .env.example .env
# Edit .env with your Twilio credentials
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Callback Server

```bash
# Terminal 1: Start ngrok to get a public URL
ngrok http 5000

# Copy the ngrok HTTPS URL into your .env as CALLBACK_URI

# Terminal 2: Start the server
python callback_server.py
```

### 4. Make a Call

```bash
python make_call.py --target +14155551234
```

## How It Works

1. `make_call.py` initiates an outbound call via Twilio API
2. When the target answers, Twilio fetches TwiML instructions from `/voice`
3. `callback_server.py` returns instructions to:
   - Say a greeting using text-to-speech
   - Pause, then say goodbye and hang up
4. Call status updates are logged via `/status` webhook

## Files

| File | Purpose |
|---|---|
| `make_call.py` | Initiate outbound phone calls |
| `callback_server.py` | Handle call events via TwiML |
| `.env.example` | Template for credentials |
