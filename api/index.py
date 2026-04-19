import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from api.bot import get_bot_response

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health():
    return {"status": "ok", "service": "GenZTech WhatsApp Bot"}, 200


@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "")
    print(f"[webhook] from={from_number} body={incoming_msg}")

    bot_reply = get_bot_response(from_number, incoming_msg)

    resp = MessagingResponse()
    resp.message(bot_reply)
    return str(resp), 200, {"Content-Type": "text/xml"}


@app.route("/cron/followup", methods=["POST", "GET"])
def cron_followup():
    """Manual trigger for follow-up reminders (for testing/demo)."""
    from api.scheduler import send_followup_reminders
    try:
        send_followup_reminders()
        return {"status": "ok", "message": "Follow-up reminders sent"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
