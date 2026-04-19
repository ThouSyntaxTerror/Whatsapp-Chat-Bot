from api.db import get_lead, upsert_lead


def get_bot_response(phone: str, user_input: str) -> str:
    """Return bot response based on user input and conversation stage."""
    user_input = user_input.strip().lower()
    lead = get_lead(phone)

    # New user → start greeting
    if lead is None:
        upsert_lead(phone, {"stage": "student_or_parent"})
        return "👋 Welcome to GenZTech! I'm here to help you find the right path.\n\nAre you a student or a parent?\n1️⃣ Student\n2️⃣ Parent"

    stage = lead.get("stage", "student_or_parent")

    # Stage: student or parent
    if stage == "student_or_parent":
        if user_input == "1":
            upsert_lead(phone, {"stage": "class_level"})
            return "Great! 📚 What's your current class/status?\n1️⃣ 10th\n2️⃣ 12th\n3️⃣ Graduate & Working Professional"
        elif user_input == "2":
            upsert_lead(phone, {"stage": "interest"})
            return "Perfect! 👨‍👩‍👧 Your child's interest?\n1️⃣ Engineering\n2️⃣ Medical\n3️⃣ Commerce\n4️⃣ AI & Tech"
        else:
            return "Sorry, I didn't get that. Please reply with 1️⃣ (Student) or 2️⃣ (Parent) 😊"

    # Stage: class level
    if stage == "class_level":
        if user_input == "1":
            upsert_lead(phone, {"stage": "city", "class_level": "10th"})
            return "Cool! 🎓 Which city are you in?"
        elif user_input == "2":
            upsert_lead(phone, {"stage": "interest", "class_level": "12th"})
            return "Awesome! What's your interest?\n1️⃣ Engineering\n2️⃣ Medical\n3️⃣ Commerce\n4️⃣ AI & Tech"
        elif user_input == "3":
            upsert_lead(phone, {"stage": "interest", "class_level": "Graduate & Working Professional"})
            return "Excellent! What interests you?\n1️⃣ Engineering\n2️⃣ Medical\n3️⃣ Commerce\n4️⃣ AI & Tech"
        else:
            return "Sorry, please reply with 1️⃣, 2️⃣, or 3️⃣ 😊"

    # Stage: interest
    if stage == "interest":
        interests = {
            "1": "Engineering",
            "2": "Medical",
            "3": "Commerce",
            "4": "AI & Tech",
        }
        if user_input in interests:
            upsert_lead(phone, {"stage": "city", "interest": interests[user_input]})
            return "Great choice! 🌟 Which city are you in?"
        else:
            return "Sorry, please reply with 1️⃣, 2️⃣, 3️⃣, or 4️⃣ 😊"

    # Stage: city
    if stage == "city":
        if user_input and len(user_input) > 0:
            upsert_lead(phone, {"stage": "completed", "city": user_input})
            # Generate qualification message based on class level
            class_level = lead.get("class_level", "")
            msg = get_qualification_message(class_level)
            upsert_lead(phone, {"booking_status": "link_sent"})
            return msg
        else:
            return "Please enter a valid city name 🏙️"

    # Stage: completed
    if stage == "completed":
        if user_input == "restart":
            upsert_lead(phone, {"stage": "student_or_parent", "booking_status": "pending"})
            return "👋 Welcome back! Let's start fresh.\n\nAre you a student or a parent?\n1️⃣ Student\n2️⃣ Parent"
        else:
            return "We already have your info! 😊 Reply RESTART to update it."

    return "Sorry, something went wrong. Reply RESTART to begin again."


def get_qualification_message(class_level: str) -> str:
    """Return qualification message based on class level."""
    import os
    calendly_link = os.environ.get("CALENDLY_LINK", "https://calendly.com/genztech/demo")
    stream_test_link = os.environ.get("STREAM_TEST_LINK", "https://genztech.pro/stream-test")

    if class_level == "10th":
        return (
            "🎯 Great! We recommend taking our **Stream Selection Test** to find your perfect career path.\n\n"
            f"📝 Start the test here: {stream_test_link}\n\n"
            "After the test, our counselor will guide you on the next steps! 🚀"
        )
    elif class_level == "12th":
        return (
            "🎯 Perfect! Let's set up a **Career Counseling Session** with our expert.\n\n"
            f"📅 Book your slot here: {calendly_link}\n\n"
            "We'll discuss your interests, career options, and help you plan your future! 🌟"
        )
    elif class_level == "Graduate & Working Professional":
        return (
            "🎯 Excellent! We have **AI & Industry 4.0 workshops** designed just for professionals like you.\n\n"
            f"📅 Book your demo here: {calendly_link}\n\n"
            "Learn cutting-edge skills and stay ahead in your career! 💼"
        )
    else:
        return (
            "🎉 Thank you for the info! A GenZTech counselor will reach out soon.\n\n"
            f"📅 Or book directly: {calendly_link}"
        )
