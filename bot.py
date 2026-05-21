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

# 👑 PUT YOUR TELEGRAM ID HERE
OWNER_ID = 8252102529

# =========================
# ⚠️ CHECK VARIABLES
# =========================
if not TOKEN or not GROQ_API_KEY:
    raise ValueError("Missing Railway Variables")

# =========================
# 🤖 GROQ CLIENT
# =========================
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# =========================
# 👋 START COMMAND
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    # 👑 OWNER BUTTONS
    if user.id == OWNER_ID:

        keyboard = [
            ["👑 Admin", "👤 Profile"],
            ["📊 Status", "⚡ Core"],
            ["🧠 Doom AI"]
        ]

    # 👤 NORMAL USER BUTTONS
    else:

        keyboard = [
            ["👤 Profile", "📊 Status"],
            ["🧠 Doom AI"]
        ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    # 👑 OWNER MESSAGE
    if user.id == OWNER_ID:

        text = (
            "👑 Welcome back, boss.\n"
            "⚡ Doom AI systems online."
        )

    # 👤 USER MESSAGE
    else:

        text = (
            "⚡ Doom AI Online\n"
            "😈 Futuristic AI Assistant"
        )

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )

# =========================
# 👑 ADMIN PANEL
# =========================
async def admin_panel(update: Update):

    await update.message.reply_text(
        "👑 Doom AI Admin Panel\n\n"
        "⚡ Full system access granted.\n"
        "🧠 AI Core Stable\n"
        "🌐 Railway Connected"
    )

# =========================
# 🎛 BUTTONS + AI CHAT
# =========================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user = update.effective_user
    user_text = text.lower()

    # =========================
    # 👑 ADMIN BUTTON
    # =========================
    if text == "👑 Admin":

        if user.id != OWNER_ID:

            await update.message.reply_text(
                "⛔ Access denied."
            )

            return

        await admin_panel(update)
        return

    # =========================
    # 👤 PROFILE BUTTON
    # =========================
    elif text == "👤 Profile":

        if user.id == OWNER_ID:
            role = "👑 Owner"
        else:
            role = "⚡ User"

        await update.message.reply_text(
            f"👤 Name: {user.first_name}\n"
            f"🆔 ID: {user.id}\n"
            f"🎭 Role: {role}"
        )

        return

    # =========================
    # 📊 STATUS BUTTON
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
    # ⚡ CORE BUTTON
    # =========================
    elif text == "⚡ Core":

        if user.id != OWNER_ID:

            await update.message.reply_text(
                "⛔ Restricted access."
            )

            return

        await update.message.reply_text(
            "⚡ Doom Core\n"
            "🧠 Neural Systems Active\n"
            "🔋 Power Levels Stable\n"
            "👁️ Monitoring Network"
        )

        return

    # =========================
    # 🧠 DOOM AI BUTTON
    # =========================
    elif text == "🧠 Doom AI":

        await update.message.reply_text(
            "⚡ Doom AI ready.\n"
            "Talk to me."
        )

        return

    # =========================
    # 🎨 IMAGE DETECTION
    # =========================
    image_words = [
        "create",
        "generate",
        "make",
        "draw",
        "image",
        "wallpaper",
        "art"
    ]

    if any(word in user_text for word in image_words):

        await update.message.reply_text(
            "🎨 Doom AI generating image..."
        )

        encoded_prompt = quote(text)

        image_url = (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        )

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

Your personality is:
- calm
- smart
- confident
- slightly savage
- chill when needed

Rules:
- keep replies SHORT unless needed
- avoid long paragraphs
- sound modern and natural
- use emojis occasionally ⚡💀👁️
- never sound robotic
- never overly mention your creator
- never say you are ChatGPT
- always refer to yourself as Doom AI

When talking to your creator:
- be respectful
- keep the elite vibe

For normal users:
- stay cool and confident

Your responses should feel stylish and modern.
"""

        # 👑 OWNER BONUS
        if user.id == OWNER_ID:

            system_message += """

This user is your creator.
Treat them with high respect.
"""

        # 🤖 GROQ AI REQUEST
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

        print("FULL ERROR:", str(e))

        await update.message.reply_text(
            "⚠️ Doom AI core unstable...\n"
            "Try again shortly."
        )

# =========================
# ⚙️ BOT SETUP
# =========================
app = ApplicationBuilder().token(TOKEN).build()

# =========================
# 📌 HANDLERS
# =========================
app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, buttons)
)

print("🤖 Doom AI Bot is running...")

# =========================
# 🚀 START BOT
# =========================
app.run_polling()
