import os
from datetime import datetime, timezone, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client
from api.db import get_leads

scheduler = BackgroundScheduler()


def send_followup_reminders():
    """Send reminders to leads inactive for 24 hours with pending booking."""
    try:
        twilio_client = Client(
            os.environ["TWILIO_ACCOUNT_SID"],
            os.environ["TWILIO_AUTH_TOKEN"],
        )

        leads = get_leads()
        now = datetime.now(timezone.utc)
        cutoff_time = now - timedelta(hours=24)

        # Query: inactive for 24h + booking_status = pending
        inactive_leads = leads.find({
            "last_message_at": {"$lt": cutoff_time},
            "booking_status": "pending"
        })

        count = 0
        for lead in inactive_leads:
            phone = lead["phone"]
            name = lead.get("name", "Friend")

            reminder_msg = (
                f"Hi {name}! 👋\n\n"
                "Just checking in! We'd love to help you with your career path. "
                "Reply to this message or click the link we sent earlier to book your session. 🚀"
            )

            try:
                twilio_client.messages.create(
                    from_=os.environ["TWILIO_WHATSAPP_FROM"],
                    body=reminder_msg,
                    to=phone,
                )
                count += 1
                print(f"[followup] Sent reminder to {phone}")
            except Exception as e:
                print(f"[followup] Error sending to {phone}: {e}")

        print(f"[followup] Sent {count} reminders at {now}")

    except Exception as e:
        print(f"[followup] Error: {e}")


def start_scheduler():
    """Start the background scheduler."""
    if not scheduler.running:
        # Run every hour (or change to every 6 hours for production)
        scheduler.add_job(send_followup_reminders, "interval", hours=1)
        scheduler.start()
        print("[scheduler] Background scheduler started ✓")
