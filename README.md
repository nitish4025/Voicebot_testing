# Voicebot Testing

Make outbound phone calls using Azure Communication Services (ACS).

## Prerequisites

1. **Azure Account** - [Create one free](https://azure.microsoft.com/free/)
2. **Azure Communication Services resource** - Create one in the Azure Portal
3. **Phone number** - Purchase a phone number in your ACS resource
4. **ngrok** - For local development callback URL

## Setup

### 1. Create Azure Communication Services Resource

1. Go to [Azure Portal](https://portal.azure.com)
2. Search for "Communication Services" and create a new resource
3. Once created, go to **Keys** → copy the **Connection string**

### 2. Get a Phone Number

1. In your ACS resource, go to **Phone numbers**
2. Click **Get a number** → select a toll-free or local number
3. Note the number in E.164 format (e.g., `+18001234567`)

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your values
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the Callback Server

```bash
# Terminal 1: Start ngrok
ngrok http 5000

# Copy the ngrok HTTPS URL into your .env as CALLBACK_URI

# Terminal 2: Start the server
python callback_server.py
```

### 6. Make a Call

```bash
python make_call.py --target +14155551234
```

## How It Works

1. `make_call.py` initiates an outbound call via Azure
2. Azure connects the call and sends webhook events to your callback server
3. `callback_server.py` handles events:
   - **CallConnected** → plays a text-to-speech greeting
   - **PlayCompleted** → hangs up the call

## Cost

- Azure Communication Services has [pay-as-you-go pricing](https://azure.microsoft.com/pricing/details/communication-services/)
- Phone number: ~$2/month (US toll-free)
- Outbound PSTN calls: ~$0.013/min (US)
