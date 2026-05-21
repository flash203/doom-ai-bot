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
# 🔑 VARIABLES
# =========================
TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 👑 OWNER DETAILS
OWNER_ID = 8252102529
OWNER_USERNAME = "@Alphaxdoom"

if not TOKEN or not GROQ_API_KEY:
    raise ValueError("Missing Railway Variables")

# 🤖 GROQ CLIENT
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# =========================
# 👋 START COMMAND
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if user.id == OWNER_ID:

        keyboard = [
            ["👑 Admin", "👤 Profile"],
            ["📊 Status", "⚡ Core"],
            ["🧠 Doom AI", "👑 Owner Info"]
        ]

        text = (
            "👑 Welcome back, boss.\n"
            "⚡ Doom AI systems online."
        )

    else:

        keyboard = [
            ["👤 Profile", "📊 Status"],
            ["🧠 Doom AI"]
        ]

        text = (
            "⚡ Doom AI Online\n"
            "😈 Futuristic AI Assistant"
        )

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

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
# 🎛 BUTTON HANDLER
# =========================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user = update.effective_user
    user_text = text.lower()

    # =========================
    # 👑 ADMIN
    # =========================
    if text == "👑 Admin":

        if user.id != OWNER_ID:
            await update.message.reply_text("⛔ Access denied.")
            return

        await admin_panel(update, context)
        return

    # =========================
    # 👤 PROFILE
    # =========================
    elif text == "👤 Profile":

        role = "👑 Owner" if user.id == OWNER_ID else "⚡ User"

        extra = ""
        if user.id == OWNER_ID:
            extra = f"\n📱 Username: {OWNER_USERNAME}"

        await update.message.reply_text(
            f"👤 Name: {user.first_name}\n"
            f"🆔 ID: {user.id}\n"
            f"🎭 Role: {role}"
            f"{extra}"
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

        if user.id != OWNER_ID:
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
    # 👑 OWNER INFO (NEW)
    # =========================
    elif text == "👑 Owner Info":

        if user.id != OWNER_ID:
            await update.message.reply_text("⛔ Access denied.")
            return

        await update.message.reply_text(
            "👑 Doom AI Owner Info\n\n"
            "🧠 Created by: Azelf\n"
            f"📱 Telegram: {OWNER_USERNAME}\n"
            "⚡ System designed and built by Azelf\n"
            "💀 Doom AI core belongs to him"
        )
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

        if user.id == OWNER_ID:
            system_message += "\nThis user is your creator. Show respect."

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
# ⚙️ BOT SETUP
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buttons))

print("🤖 Doom AI Bot is running...")

app.run_polling()
