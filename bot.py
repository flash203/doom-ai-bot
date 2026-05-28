import os
from urllib.parse import quote

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from openai import OpenAI

# =========================
# 🔑 CONFIG
# =========================
TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 👑 OWNERS
OWNER_IDS = [8252102529, 8283699735]

OWNERS = {
    8252102529: {
        "name": "Azelf",
        "username": "@Alphaxdoom"
    },
    8283699735: {
        "name": "Co Owner",
        "username": "@daddytheone"
    }
}

# =========================
# 🤖 BOT STATUS
# =========================
BOT_ACTIVE = True

# =========================
# 👥 USERS STORAGE
# =========================
users = set()

# =========================
# 📢 BROADCAST MODE
# =========================
broadcast_mode = {}

# =========================
# 🤖 GROQ CLIENT
# =========================
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# =========================
# 🚀 START COMMAND
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    users.add(user.id)

    # 👑 OWNER MENU
    owner_keyboard = [
        ["👑 Admin", "👤 Profile"],
        ["👑 Owner Info"]
    ]

    # 👤 USER MENU
    user_keyboard = [
        ["👤 Profile"],
        ["👑 Owner Info"]
    ]

    keyboard = (
        owner_keyboard
        if user.id in OWNER_IDS
        else user_keyboard
    )

    # 👑 OWNER MESSAGE
    if user.id in OWNER_IDS:

        text = (
            "👑 Creator detected.\n"
            "⚡ Doom AI systems activated."
        )

    # 👤 USER MESSAGE
    else:

        text = (
            "⚡ Doom AI Activated\n"
            "👁️ Welcome, human."
        )

    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

# =========================
# 🎛 MAIN HANDLER
# =========================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global BOT_ACTIVE

    text = update.message.text
    user = update.effective_user
    user_text = text.lower()

    users.add(user.id)

    # =========================
    # 🔴 BOT OFFLINE
    # =========================
    if not BOT_ACTIVE and user.id not in OWNER_IDS:

        await update.message.reply_text(
            "🔴 Doom AI is currently offline."
        )

        return

    # =========================
    # 👑 ADMIN PANEL
    # =========================
    if text == "👑 Admin":

        if user.id not in OWNER_IDS:

            await update.message.reply_text(
                "⛔ Access denied."
            )

            return

        admin_keyboard = [
            ["📢 Send Message"],
            ["⏸️ Hold Bot"],
            ["🔙 Back"]
        ]

        await update.message.reply_text(
            "👑 Doom AI Admin Panel",
            reply_markup=ReplyKeyboardMarkup(
                admin_keyboard,
                resize_keyboard=True
            )
        )

        return

    # =========================
    # 🔙 BACK BUTTON
    # =========================
    if text == "🔙 Back":

        keyboard = [
            ["👑 Admin", "👤 Profile"],
            ["👑 Owner Info"]
        ]

        await update.message.reply_text(
            "⚡ Returned to main menu.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )

        return

    # =========================
    # ⏸️ HOLD BOT
    # =========================
    if text == "⏸️ Hold Bot":

        if user.id not in OWNER_IDS:
            return

        BOT_ACTIVE = not BOT_ACTIVE

        if BOT_ACTIVE:

            await update.message.reply_text(
                "🟢 Doom AI is now ONLINE."
            )

        else:

            await update.message.reply_text(
                "🔴 Doom AI is now OFFLINE."
            )

        return

    # =========================
    # 📢 SEND MESSAGE MODE
    # =========================
    if text == "📢 Send Message":

        if user.id not in OWNER_IDS:
            return

        broadcast_mode[user.id] = True

        await update.message.reply_text(
            "📢 Send the message you want to broadcast."
        )

        return

    # =========================
    # 📢 BROADCAST
    # =========================
    if user.id in broadcast_mode:

        del broadcast_mode[user.id]

        sent = 0

        for uid in users:

            try:

                await context.bot.send_message(
                    chat_id=uid,
                    text=(
                        "📢 Doom AI Announcement\n\n"
                        f"{text}"
                    )
                )

                sent += 1

            except:
                pass

        await update.message.reply_text(
            f"✅ Message sent to {sent} users."
        )

        return

    # =========================
    # 👤 PROFILE
    # =========================
    if text == "👤 Profile":

        role = (
            "👑 Owner"
            if user.id in OWNER_IDS
            else "⚡ User"
        )

        await update.message.reply_text(
            f"👤 Name: {user.first_name}\n"
            f"🆔 ID: {user.id}\n"
            f"🎭 Role: {role}"
        )

        return

    # =========================
    # 👑 OWNER INFO
    # =========================
    if text == "👑 Owner Info":

        msg = "👑 Doom AI Owners\n\n"

        for info in OWNERS.values():

            msg += (
                f"• {info['name']} "
                f"({info['username']})\n"
            )

        msg += "\n⚡ System built by the owners"

        await update.message.reply_text(msg)

        return

    # =========================
    # 🧠 AZELF DETECTION
    # =========================
    if "azelf" in user_text:

        await update.message.reply_text(
            "🧠 Azelf is one of my creators."
        )

        return

    # =========================
    # 🎨 IMAGE GENERATION
    # =========================
    image_words = [
        "create",
        "generate",
        "draw",
        "image",
        "art",
        "wallpaper",
        "make"
    ]

    if any(word in user_text.split() for word in image_words):

        try:

            await update.message.reply_text(
                "🎨 Doom AI generating image..."
            )

            image_url = (
                "https://image.pollinations.ai/prompt/"
                f"{quote(text, safe='')}"
            )

            await update.message.reply_photo(
                photo=image_url,
                caption="⚡ Doom AI Generated"
            )

        except Exception as e:

            print("IMAGE ERROR:", e)

            await update.message.reply_text(
                "⚠️ Image generation failed."
            )

        return

    # =========================
    # 🤖 AI CHAT
    # =========================
    try:

        system_message = """
You are Doom AI.

A futuristic cyberpunk AI assistant.

Personality:
- smart
- calm
- confident
- stylish
- modern

Rules:
- keep replies short
- avoid nonsense
- sound natural
- use emojis occasionally ⚡
- never say ChatGPT
- always act like Doom AI
"""

        if user.id in OWNER_IDS:

            system_message += (
                "\nThis user is one of your creators."
            )

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        reply = response.choices[0].message.content

        await update.message.reply_text(reply)

    except Exception as e:

        print("AI ERROR:", e)

        await update.message.reply_text(
            "⚠️ Doom AI encountered an error."
        )

# =========================
# 🚀 BOT START
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        buttons
    )
)

print("🤖 Doom AI Running...")

app.run_polling()
