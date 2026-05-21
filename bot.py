import os
import json
from urllib.parse import quote
from datetime import datetime

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
# 🔑 VARIABLES
# =========================
TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 👑 MULTI OWNERS
OWNER_IDS = [8252102529, 8283699735]

OWNERS = {
    8252102529: {
        "name": "Azelf",
        "username": "@Alphaxdoom"
    },
    8283699735: {
        "name": "The one",
        "username": "@daddytheone"
    }
}

USER_LOG_FILE = "users.json"

if not TOKEN or not GROQ_API_KEY:
    raise ValueError("Missing Railway Variables")

# 🤖 GROQ CLIENT
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# =========================
# 🧠 USER LOGGER
# =========================
def log_user(user):
    try:
        try:
            with open(USER_LOG_FILE, "r") as f:
                data = json.load(f)
        except:
            data = {}

        data[str(user.id)] = {
            "name": user.first_name,
            "username": user.username,
            "last_seen": str(datetime.now())
        }

        with open(USER_LOG_FILE, "w") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print("LOG ERROR:", e)


# =========================
# 👋 START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    owner_keyboard = [
        ["👑 Admin", "👤 Profile"],
        ["📊 Status", "⚡ Core"],
        ["🧠 Doom AI", "👑 Owner Info"],
        ["👥 Users"]
    ]

    user_keyboard = [
        ["👤 Profile", "📊 Status"],
        ["🧠 Doom AI"],
        ["👑 Owner Info"]
    ]

    if user.id in OWNER_IDS:
        keyboard = owner_keyboard
        text = "👑 Welcome back, boss.\n⚡ Doom AI systems online."
    else:
        keyboard = user_keyboard
        text = "⚡ Doom AI Online\n😈 Futuristic AI Assistant"

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(text, reply_markup=reply_markup)


# =========================
# 👑 ADMIN PANEL
# =========================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👑 Doom AI Admin Panel\n\n"
        "⚡ Full system access granted.\n"
        "🧠 AI Core Stable\n"
        "🌐 Railway Connected"
    )


# =========================
# 🎛 BUTTONS
# =========================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user = update.effective_user
    user_text = text.lower()

    log_user(user)

    # =========================
    # 👑 ADMIN
    # =========================
    if text == "👑 Admin":

        if user.id not in OWNER_IDS:
            await update.message.reply_text("⛔ Access denied.")
            return

        await admin_panel(update, context)
        return

    # =========================
    # 👤 PROFILE
    # =========================
    elif text == "👤 Profile":

        role = "👑 Owner" if user.id in OWNER_IDS else "⚡ User"

        await update.message.reply_text(
            f"👤 Name: {user.first_name}\n"
            f"🆔 ID: {user.id}\n"
            f"🎭 Role: {role}"
        )
        return

    # =========================
    # 📊 STATUS
    # =========================
    elif text == "📊 Status":

        await update.message.reply_text(
            "✅ Doom AI Status\n"
            "⚡ Systems Online\n"
            "🧠 AI Core Active\n"
            "🌐 Railway Stable"
        )
        return

    # =========================
    # ⚡ CORE
    # =========================
    elif text == "⚡ Core":

        if user.id not in OWNER_IDS:
            await update.message.reply_text("⛔ Restricted access.")
            return

        await update.message.reply_text(
            "⚡ Doom Core\n"
            "🧠 Neural Systems Active\n"
            "🔋 Power Levels Stable\n"
            "👁️ Monitoring Network"
        )
        return

    # =========================
    # 🧠 DOOM AI
    # =========================
    elif text == "🧠 Doom AI":

        await update.message.reply_text(
            "⚡ Doom AI ready.\nTalk to me."
        )
        return

    # =========================
    # 👑 OWNER INFO (PUBLIC)
    # =========================
    elif text == "👑 Owner Info":

        msg = "👑 Doom AI Owners\n\n"

        for owner_id, info in OWNERS.items():
            msg += f"• {info['name']} ({info['username']})\n"

        msg += "\n⚡ System built and managed by the owners"

        await update.message.reply_text(msg)
        return

    # =========================
    # 👥 USERS (OWNER ONLY)
    # =========================
    elif text == "👥 Users":

        if user.id not in OWNER_IDS:
            await update.message.reply_text("⛔ Access denied.")
            return

        try:
            with open(USER_LOG_FILE, "r") as f:
                data = json.load(f)

            msg = "👥 Doom AI Users:\n\n"

            for uid, info in data.items():
                msg += (
                    f"🆔 {uid}\n"
                    f"👤 {info['name']}\n"
                    f"📱 @{info['username']}\n"
                    f"⏰ {info['last_seen']}\n\n"
                )

            await update.message.reply_text(msg[:4000])

        except:
            await update.message.reply_text("No users found yet.")
        return

    # =========================
    # 🧠 AZELF DETECTION
    # =========================
    if "azelf" in user_text:

        await update.message.reply_text(
            "🧠 Azelf is my creator.\n"
            "⚡ The one who built and designed Doom AI."
        )
        return

    # =========================
    # 🎨 IMAGE GENERATION
    # =========================
    image_words = ["create", "generate", "make", "draw", "image", "wallpaper", "art"]

    if any(word in user_text.split() for word in image_words):

        await update.message.reply_text("🎨 Doom AI generating image...")

        encoded_prompt = quote(text, safe="")

        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

        await update.message.reply_photo(
            photo=image_url,
            caption="⚡ Doom AI Image Generated"
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
- calm
- smart
- confident
- slightly savage
- chill

Rules:
- keep replies SHORT
- sound natural
- use emojis sometimes ⚡💀👁️
- never say ChatGPT
- always call yourself Doom AI
"""

        if user.id in OWNER_IDS:
            system_message += "\nThis user is one of your creators. Show respect."

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": text}
            ]
        )

        reply = response.choices[0].message.content

        await update.message.reply_text(reply)

    except Exception as e:
        print("ERROR:", str(e))

        await update.message.reply_text(
            "⚠️ Doom AI core unstable...\nTry again."
        )


# =========================
# ⚙️ BOT START
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buttons))

print("🤖 Doom AI Bot is running...")

app.run_polling()
