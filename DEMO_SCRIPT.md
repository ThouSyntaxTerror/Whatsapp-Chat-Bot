# GenZTech WhatsApp Bot — Demo Video Script (5–7 min)

## Structure
1. **Intro** (0:00–0:30) — Show problem + solution
2. **Live Demo** (0:30–3:00) — Full conversation flow
3. **Follow-up Trigger** (3:00–3:30) — Manual reminder
4. **Code Walkthrough** (3:30–5:30) — Key components
5. **Deployment & Wrap-up** (5:30–7:00) — Live URL + next steps

---

## 📹 Part 1: Intro (0:00–0:30)

**On Screen:** Project folder open (show file structure)

**Script:**
> "Hi, I'm Atharv. This is the GenZTech WhatsApp Bot — an AI-powered solution to automate student lead follow-ups.
>
> **The problem:** Manual WhatsApp follow-ups are slow and inconsistent.
>
> **Our solution:** A chatbot that:
> - Captures student info automatically
> - Qualifies leads based on class & interests
> - Sends booking links to Calendly
> - Follows up with inactive users after 24 hours
>
> Let me show you how it works."

---

## 💬 Part 2: Live Demo (0:30–3:00)

**Setup:** Have your phone ready with WhatsApp open to the bot conversation thread.

### 2.1: Start Fresh (0:30–1:00)
**On Screen:** Show WhatsApp conversation

**Script & Actions:**
> "First, let me start a fresh conversation by typing 'restart'."

**Send:** `restart`  
**Bot replies:** "👋 Welcome back! Student or parent? 1️⃣ 2️⃣"

> "Great! Let me go through the student path. I'll reply with 1."

### 2.2: Class Selection (1:00–1:30)
**Send:** `1`  
**Bot replies:** "What's your class? 1️⃣ 10th 2️⃣ 12th 3️⃣ Graduate"

**Script:**
> "The bot asks what class I'm in. I'm a 12th class student, so I'll reply with 2."

**Send:** `2`

### 2.3: Interest Selection (1:30–2:00)
**Bot replies:** "What's your interest? 1️⃣ Engineering 2️⃣ Medical 3️⃣ Commerce 4️⃣ AI & Tech"

**Script:**
> "Now it asks about my interests. I'm interested in AI & Tech, so 4."

**Send:** `4`

### 2.4: City & Qualification (2:00–3:00)
**Bot replies:** "Which city are you in?"

**Script:**
> "Next, I enter my city."

**Send:** `Pune`

**Bot replies:** "🎯 Let's set up Career Counseling! 📅 Book your slot: https://calendly.com/genztech/demo-session ... "

**Script:**
> "Perfect! The bot recognizes I'm a 12th class student and sends the career counseling booking link. 
>
> The entire lead capture took just seconds — no manual effort needed. The lead is now stored in MongoDB with all their info ready for our team."

---

## 🔄 Part 3: Follow-up Automation (3:00–3:30)

**On Screen:** Vercel dashboard or browser console

**Script:**
> "Now let's trigger the follow-up automation. We have a scheduler that runs every hour and sends reminders to leads who haven't responded in 24 hours.
>
> Let me manually trigger it for the demo."

**Action:** Open browser to `https://genztech-whatsapp-bot.vercel.app/cron/followup`

**Script:**
> "When I hit this endpoint, the scheduler queries our MongoDB for inactive leads and sends them a reminder via Twilio.
> 
> This happens automatically every hour — so leads never slip through the cracks."

---

## 💻 Part 4: Code Walkthrough (3:30–5:30)

**On Screen:** Code editor with these files open

### 4.1: Bot Logic (3:30–4:00)
**File:** `api/bot.py`

**Script:**
> "Let me show you the brain of the bot — the conversation logic. 
>
> We use a state machine approach. Each user has a 'stage' field in the database:
> - student_or_parent
> - class_level
> - interest
> - city
> - completed
>
> As the user progresses through the conversation, we update their stage and continue from there. This makes it easy to handle pauses or come back later."

**Highlight:** The `get_bot_response()` function and stage checks.

### 4.2: Database Connection (4:00–4:30)
**File:** `api/db.py`

**Script:**
> "All lead data is stored in MongoDB Atlas. We use `upsert_lead()` to insert or update leads by their phone number.
>
> Every interaction updates the `last_message_at` timestamp — this is key for our follow-up system."

**Highlight:** The `upsert_lead()` function and MongoDB schema.

### 4.3: Follow-up Automation (4:30–5:00)
**File:** `api/scheduler.py`

**Script:**
> "The scheduler runs a background job that queries MongoDB for leads inactive for 24+ hours, then sends them a reminder via Twilio.
>
> It's simple but powerful — zero manual follow-ups needed."

**Highlight:** The `send_followup_reminders()` function.

### 4.4: Deployment (5:00–5:30)
**On Screen:** Vercel dashboard

**Script:**
> "The entire bot is deployed on Vercel — a serverless platform. This means:
> - No servers to manage
> - Automatic scaling
> - Free tier covers our use case
> - Instant updates when we push code
>
> The bot is live at: genztech-whatsapp-bot.vercel.app"

---

## 🎯 Part 5: Wrap-up (5:30–7:00)

**On Screen:** GitHub repo (or project folder)

**Script:**
> "Let me summarize what we've built:
>
> ✅ **Automated Lead Capture** — No more manual typing  
> ✅ **Smart Qualification** — Routes students based on profile  
> ✅ **Instant Booking Links** — Calendly integration  
> ✅ **Automatic Follow-ups** — Reminders after 24 hours  
> ✅ **Scalable** — Handles hundreds of leads  
>
> **Tech Stack:**
> - Twilio WhatsApp API
> - Python + Flask
> - MongoDB for persistence
> - APScheduler for automation
> - Vercel for deployment
>
> All code is on GitHub: [link]
> Live bot: https://genztech-whatsapp-bot.vercel.app
>
> This assignment has given me hands-on experience with:
> - API integrations (Twilio, MongoDB)
> - State machine design
> - Background job scheduling
> - Serverless deployment
>
> Thanks for watching! Questions?"

---

## 📋 Recording Checklist

- [ ] Phone charged & WhatsApp open
- [ ] Vercel dashboard logged in
- [ ] Code editor open with key files
- [ ] Internet connection stable
- [ ] Microphone working
- [ ] Screen recording tool ready (OBS, ScreenFlow, etc.)
- [ ] Quiet environment
- [ ] Test one message flow before recording

---

## ⏱️ Timing Guide

| Section | Duration | Cumulative |
|---------|----------|-----------|
| Intro | 0:30 | 0:30 |
| Live Demo | 2:30 | 3:00 |
| Follow-up Trigger | 0:30 | 3:30 |
| Code Walkthrough | 2:00 | 5:30 |
| Wrap-up | 1:30 | 7:00 |

---

## 🎬 Recording Tips

1. **Start with a test message** before hitting record — make sure bot is responsive
2. **Speak clearly** — this is an assignment submission, not a casual video
3. **Pause slightly** when transitioning between sections
4. **Show the live URL** at least once so evaluators can test it
5. **Don't speed up** — let each interaction be visible
6. **One mistake?** Just redo that section and edit it in post
7. **Aim for 5–7 min** — not much shorter, not much longer

---

## 📤 Submission Format

Export video as:
- **Format:** MP4 or WebM
- **Resolution:** 1080p (or 720p minimum)
- **Frame rate:** 30fps
- **File size:** Keep under 500MB (use YouTube compression if needed)
- **Upload to:** Google Drive → share link in Google Group

---

## 🎓 Key Talking Points

Remember to emphasize:
1. **Problem solved** — automation saves time
2. **Technical depth** — multi-component system
3. **User experience** — natural conversation flow
4. **Production-ready** — deployed & tested
5. **Scalability** — can handle many leads
6. **Learning** — what you built & why

Good luck! 🚀
