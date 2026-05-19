from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from openai import OpenAI
import os

# 🔑 Railway environment variables
TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🤖 Groq client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# 👋 Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Doom AI Bot is online!"
    )

# 💬 AI chat
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are a smart helpful AI assistant."
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
        print(e)
        await update.message.reply_text(
            "⚠️ AI failed."
        )

# ⚙️ Telegram bot setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
)

print("🤖 Doom AI Bot is running...")

app.run_polling()