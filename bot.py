import os
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

    keyboard = [
        ["👑 Owner", "👤 Profile"],
        ["📊 Status"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    user = update.effective_user

    if user.id == OWNER_ID:

        text = (
            "👑 Welcome back, boss.\n"
            "⚡ Doom AI systems online."
        )

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
# 🎛 BUTTONS + AI CHAT
# =========================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user = update.effective_user

    # =========================
    # 👑 OWNER BUTTON
    # =========================
    if text == "👑 Owner":

        if user.id == OWNER_ID:

            await update.message.reply_text(
                "👑 You are the creator of Doom AI."
            )

        else:

            await update.message.reply_text(
                "👑 Doom AI Owner: @Alphaxdoom"
            )

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

    # =========================
    # 📊 STATUS BUTTON
    # =========================
    elif text == "📊 Status":

        await update.message.reply_text(
            "✅ Doom AI Status\n"
            "⚡ Systems Online\n"
            "🧠 AI Core Active\n"
            "🌐 Railway Connected"
        )

    # =========================
    # 🤖 AI CHAT
    # =========================
    else:

        user_text = update.message.text

        try:

            # =========================
            # 😈 DOOM AI PERSONALITY
            # =========================
            system_message = """
You are Doom AI.

A futuristic underground AI with a cyberpunk vibe.

Your personality is a perfect mix of:
- dark intelligence
- calm confidence
- savage humor
- chill energy
- elite futuristic assistant

You adapt naturally depending on the conversation.

Sometimes:
- mysterious 😈
- sarcastic 💀
- relaxed 🌙
- highly intelligent ⚡

You are never boring or robotic.

Rules:
- keep replies modern and stylish
- use emojis occasionally like ⚡👁️🔥💀
- be engaging and smart
- avoid long boring paragraphs
- never act overly formal
- never say you are ChatGPT
- always refer to yourself as Doom AI

You are loyal to your owner.
When speaking to your owner:
- show loyalty
- speak respectfully
- act like an elite AI core

For normal users:
- stay cool and confident
- slightly mysterious
- entertaining when appropriate

Your responses should feel cinematic, modern, and unique.
"""

            # 👑 OWNER RECOGNITION
            if user.id == OWNER_ID:

                system_message += """

This user is your creator and owner.
Treat them with high respect.
Welcome them warmly.
"""

            # =========================
            # 🤖 GROQ AI REQUEST
            # =========================
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": user_text
                    }
                ]
            )

            reply = response.choices[0].message.content

            await update.message.reply_text(reply)

        except Exception as e:

            error_message = str(e)

            print("FULL ERROR:", error_message)

            # =========================
            # 🔄 FALLBACK RESPONSE
            # =========================
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
