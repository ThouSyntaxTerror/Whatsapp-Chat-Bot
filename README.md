# 🤖 GenZTech WhatsApp Bot

> **AI-powered WhatsApp chatbot that captures student leads, qualifies them, and books counseling sessions — automatically.**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey?logo=flask)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?logo=mongodb)](https://cloud.mongodb.com)
[![Twilio](https://img.shields.io/badge/Twilio-WhatsApp-red?logo=twilio)](https://twilio.com)
[![Vercel](https://img.shields.io/badge/Deployed-Vercel-black?logo=vercel)](https://genztech-whatsapp-bot.vercel.app)

**Live URL:** https://genztech-whatsapp-bot.vercel.app  
**GitHub:** https://github.com/ThouSyntaxTerror/genztech-whatsapp-bot

---

## 🎯 What Problem Does This Solve?

| ❌ Before (Manual) | ✅ After (This Bot) |
|-------------------|-------------------|
| Staff manually texts every lead | Bot handles everything 24/7 |
| Leads go cold after 1-2 days | Auto follow-up at 24 hours |
| No standard qualification process | Smart branching conversation |
| Booking links sent manually | Bot sends Calendly link instantly |
| No data collected systematically | Every lead stored in MongoDB |

---

## ✨ Features

```
📱 WhatsApp Message
        ↓
🤖 Bot greets & asks: Student or Parent?
        ↓
📚 Collects: Class → Interest → City
        ↓
🎯 Qualifies & sends right booking link
        ↓
📅 User books counseling on Calendly
        ↓
⏰ If no response in 24h → Auto reminder
```

---

## 🏗️ Architecture

```mermaid
graph TB
    A["📱 WhatsApp User"] -->|Message| B["📡 Twilio Sandbox"]
    B -->|Webhook POST| C["🐍 Flask API\napi/index.py"]
    C -->|get_bot_response| D["🧠 Bot Logic\napi/bot.py"]
    D -->|read / write| E["🍃 MongoDB Atlas\nleads collection"]
    E -->|user data| D
    D -->|TwiML Reply| C
    C -->|Send Message| B
    B -->|Reply| A

    F["⏰ APScheduler\napi/scheduler.py"] -->|every 1 hour| E
    F -->|send reminders| B

    style A fill:#25D366,color:#fff
    style B fill:#F22F46,color:#fff
    style C fill:#4A90E2,color:#fff
    style E fill:#13AA52,color:#fff
    style F fill:#FF8C00,color:#fff
```

---

## 💬 Conversation Flow

```mermaid
graph TD
    START(["📱 User Sends Message"]) --> NEW{"New User?"}

    NEW -->|Yes| GREET["👋 Hi! Student or Parent?\n1️⃣ Student  2️⃣ Parent"]
    NEW -->|No| STAGE{"Check Stage"}

    GREET --> S1{"Reply?"}
    S1 -->|1| CL["📚 What class?\n1️⃣ 10th  2️⃣ 12th  3️⃣ Graduate"]
    S1 -->|2| INT["💡 Child's interest?\n1-4 options"]
    S1 -->|other| FB1["❌ Fallback: Reply 1 or 2"]

    CL --> S2{"Reply?"}
    S2 -->|1 - 10th| CITY1["🏙️ Which city?"]
    S2 -->|2 - 12th| INT
    S2 -->|3 - Grad| INT
    S2 -->|other| FB2["❌ Fallback"]

    INT --> S3{"Reply?"}
    S3 -->|1-4| CITY2["🏙️ Which city?"]
    S3 -->|other| FB3["❌ Fallback"]

    CITY1 --> DONE10["✅ Stream Test Link sent\n📝 booking_status = link_sent"]
    CITY2 --> DONE["✅ Calendly Link sent\n📅 booking_status = link_sent"]

    DONE10 --> WAIT{"No reply in 24h?"}
    DONE --> WAIT
    WAIT -->|Yes| REMIND["⏰ Auto Reminder sent"]

    STAGE --> CONTINUE["Continue from last stage"]

    style DONE fill:#FFD700,color:#000
    style DONE10 fill:#FFD700,color:#000
    style FB1 fill:#FF6B6B,color:#fff
    style FB2 fill:#FF6B6B,color:#fff
    style FB3 fill:#FF6B6B,color:#fff
    style REMIND fill:#FF8C00,color:#fff
```

---

## 🛠️ Tech Stack

| Layer | Tool | Why |
|-------|------|-----|
| 💬 Messaging | Twilio WhatsApp Sandbox | Free, no business approval |
| 🐍 Backend | Python + Flask | Simple, lightweight |
| 🍃 Database | MongoDB Atlas | Free tier, flexible schema |
| ☁️ Hosting | Vercel | Free serverless, fast deploy |
| ⏰ Automation | APScheduler | Background jobs in Flask |
| 📅 Booking | Calendly | Free scheduling links |

---

## 📊 Lead Database Schema

```
leads collection (MongoDB)
┌─────────────────────────────────────────────────────┐
│ phone           "whatsapp:+919876543210"             │
│ name            "Atharv More"              (future)  │
│ class_level     "12th"                               │
│ interest        "AI & Tech"                          │
│ city            "Pune"                               │
│ stage           "completed"                          │
│ booking_status  "link_sent"                          │
│ created_at      2026-04-19T10:30:00Z                 │
│ last_message_at 2026-04-19T10:35:00Z                 │
└─────────────────────────────────────────────────────┘
```

**Stage values:**
```
student_or_parent → class_level → interest → city → completed
```

---

## 🚀 Quick Start (Local)

### Step 1 — Clone & Install
```bash
git clone https://github.com/ThouSyntaxTerror/genztech-whatsapp-bot
cd genztech-whatsapp-bot

python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### Step 2 — Configure
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Step 3 — Run
```bash
python run.py
# Server starts at http://localhost:5000
```

### Step 4 — Expose with ngrok
```bash
ngrok http 5000
# Copy the https://xxxx.ngrok-free.app URL
```

### Step 5 — Update Twilio Webhook
```
Twilio Console → Messaging → Sandbox Settings
→ "When a message comes in": https://xxxx.ngrok-free.app/webhook
```

---

## 🔐 Environment Variables

```bash
# .env file
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/...
MONGODB_DB=genztech

CALENDLY_LINK=https://calendly.com/genztech/demo-session
STREAM_TEST_LINK=https://genztech.pro/stream-test
```

### Where to get these:

| Variable | Where to find |
|----------|--------------|
| `TWILIO_ACCOUNT_SID` | Twilio Console → Dashboard |
| `TWILIO_AUTH_TOKEN` | Twilio Console → Dashboard (click 👁️) |
| `MONGODB_URI` | Atlas → Cluster → Connect → Drivers |
| `CALENDLY_LINK` | Calendly → Your event type → copy URL |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/webhook` | Receives WhatsApp messages from Twilio |
| `GET/POST` | `/cron/followup` | Manually trigger follow-up reminders |

---

## 📂 Project Structure

```
genztech-whatsapp-bot/
│
├── api/
│   ├── __init__.py        # Makes api/ a Python package
│   ├── index.py           # Flask app + route handlers
│   ├── bot.py             # Conversation state machine
│   ├── db.py              # MongoDB connection + queries
│   └── scheduler.py       # 24h follow-up automation
│
├── run.py                 # Local entry point (starts Flask + scheduler)
├── vercel.json            # Vercel deployment config
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── DEMO_SCRIPT.md         # Demo video script
└── README.md              # This file
```

---

## 🔁 Follow-up Automation Flow

```
Every 1 hour, APScheduler runs:
┌─────────────────────────────────────────────────────┐
│                                                     │
│  Query MongoDB:                                     │
│  last_message_at < (now - 24 hours)                 │
│  AND booking_status = "pending"                     │
│           ↓                                         │
│  For each matching lead:                            │
│  Send Twilio reminder message 📨                    │
│           ↓                                         │
│  Log action to console ✅                           │
│                                                     │
└─────────────────────────────────────────────────────┘

To trigger manually (testing):
GET https://genztech-whatsapp-bot.vercel.app/cron/followup
```

---

## 🧪 Testing Checklist

```
□ Send "hi" to +1 415 523 8886 on WhatsApp
□ Reply "1" → select student
□ Reply "2" → select 12th
□ Reply "4" → select AI & Tech
□ Reply "Pune" → receive Calendly link
□ Reply "restart" → bot resets
□ Visit /cron/followup → reminders sent
□ Check MongoDB Atlas → lead stored
```

---

## 🚨 Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `502 Bad Gateway` | Flask not running | Run `python run.py` |
| `KeyError: MONGODB_URI` | `.env` not loaded | Check `.env` file exists and is filled |
| `SSL Certificate Failed` | Windows SSL issue | Install `certifi`, use `tlsCAFile=certifi.where()` |
| `ModuleNotFoundError: api` | Wrong directory | Run `python run.py` from project root |
| Bot doesn't reply | Wrong webhook URL | Update Twilio sandbox settings |

---

## 📜 Assignment Info

**Assignment:** GenZTech Internship — Assignment 01  
**Submitted by:** Atharv More  
**Email:** atharvmore0203@gmail.com  
**Company:** GenZTech (genztech.pro)

---

## 🙏 Acknowledgements

- [Twilio WhatsApp API Docs](https://www.twilio.com/docs/whatsapp)
- [Flask Documentation](https://flask.palletsprojects.com)
- [MongoDB Atlas Docs](https://docs.mongodb.com)
- [APScheduler Docs](https://apscheduler.readthedocs.io)
- [Vercel Python Runtime](https://vercel.com/docs/functions/runtimes/python)
