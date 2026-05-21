import os
import time
import sqlite3
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

OWNER_IDS = [8252102529, 8283699735]

OWNERS = {
    8252102529: {"name": "Azelf", "username": "@Alphaxdoom"},
    8283699735: {"name": "The one", "username": "@daddytheone"}
}

if not TOKEN or not GROQ_API_KEY:
    raise ValueError("Missing variables")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# =========================
# 🧠 SQLITE DATABASE
# =========================
db = sqlite3.connect("doom.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    username TEXT,
    last_seen TEXT,
    banned INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    user_id INTEGER PRIMARY KEY,
    last_message TEXT
)
""")

db.commit()

# =========================
# 🧠 DB FUNCTIONS
# =========================
def save_user(user):
    cursor.execute("""
    INSERT OR REPLACE INTO users (user_id, name, username, last_seen)
    VALUES (?, ?, ?, ?)
    """, (user.id, user.first_name, user.username, time.ctime()))
    db.commit()

def is_banned(user_id):
    cursor.execute("SELECT banned FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    return row and row[0] == 1

def ban_user(user_id):
    cursor.execute("UPDATE users SET banned=1 WHERE user_id=?", (user_id,))
    db.commit()

def unban_user(user_id):
    cursor.execute("UPDATE users SET banned=0 WHERE user_id=?", (user_id,))
    db.commit()

def save_memory(user_id, text):
    cursor.execute("""
    INSERT OR REPLACE INTO memory (user_id, last_message)
    VALUES (?, ?)
    """, (user_id, text))
    db.commit()

def get_memory(user_id):
    cursor.execute("SELECT last_message FROM memory WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else ""

def get_user_count():
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]

# =========================
# 🚀 START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    owner_keyboard = [
        ["👑 Admin", "👤 Profile"],
        ["📊 Status", "⚡ Core"],
        ["🧠 Doom AI", "👑 Owner Info"],
        ["👥 Users", "🚫 Ban", "✅ Unban"]
    ]

    user_keyboard = [
        ["👤 Profile", "📊 Status"],
        ["🧠 Doom AI"],
        ["👑 Owner Info"]
    ]

    keyboard = owner_keyboard if user.id in OWNER_IDS else user_keyboard

    await update.message.reply_text(
        "💀 Doom AI Pro v5 Online",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# =========================
# 🎛 HANDLER
# =========================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user = update.effective_user
    user_text = text.lower()

    # 🚫 banned check
    if is_banned(user.id):
        await update.message.reply_text("⛔ You are banned.")
        return

    save_user(user)

    # =========================
    # 👤 PROFILE
    # =========================
    if text == "👤 Profile":
        role = "👑 Owner" if user.id in OWNER_IDS else "⚡ User"

        await update.message.reply_text(
            f"👤 Name: {user.first_name}\n"
            f"🆔 {user.id}\n"
            f"🎭 {role}"
        )
        return

    # =========================
    # 📊 STATUS
    # =========================
    if text == "📊 Status":
        await update.message.reply_text(
            f"💀 Doom AI v5\n"
            f"👥 Users: {get_user_count()}\n"
            f"⚡ Online"
        )
        return

    # =========================
    # 👑 OWNER INFO
    # =========================
    if text == "👑 Owner Info":
        msg = "👑 Owners\n\n"
        for o in OWNERS.values():
            msg += f"• {o['name']} ({o['username']})\n"

        await update.message.reply_text(msg)
        return

    # =========================
    # 👥 USERS (OWNER ONLY)
    # =========================
    if text == "👥 Users":

        if user.id not in OWNER_IDS:
            await update.message.reply_text("⛔ Access denied.")
            return

        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        msg = "👥 Users List\n\n"
        for r in rows:
            msg += f"{r[0]} | {r[1]} | @{r[2]} | banned={r[4]}\n"

        await update.message.reply_text(msg[:4000])
        return

    # =========================
    # 🚫 BAN
    # =========================
    if text == "🚫 Ban":

        if user.id not in OWNER_IDS:
            return

        try:
            target = int(context.args[0])
            ban_user(target)
            await update.message.reply_text(f"🚫 Banned {target}")
        except:
            await update.message.reply_text("Usage: /ban USER_ID")
        return

    # =========================
    # ✅ UNBAN
    # =========================
    if text == "✅ Unban":

        if user.id not in OWNER_IDS:
            return

        try:
            target = int(context.args[0])
            unban_user(target)
            await update.message.reply_text(f"✅ Unbanned {target}")
        except:
            await update.message.reply_text("Usage: /unban USER_ID")
        return

    # =========================
    # 🧠 MEMORY
    # =========================
    save_memory(user.id, text)
    memory = get_memory(user.id)

    # =========================
    # 🎨 IMAGE
    # =========================
    if any(w in user_text for w in ["create", "draw", "image", "art"]):
        url = f"https://image.pollinations.ai/prompt/{quote(text, safe='')}"
        await update.message.reply_photo(photo=url)
        return

    # =========================
    # 🤖 AI
    # =========================
    try:

        system = f"""
You are Doom AI v5.

Short, smart, powerful.

Memory: {memory}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": text}
            ]
        )

        await update.message.reply_text(
            response.choices[0].message.content
        )

    except:
        await update.message.reply_text("⚠️ Error")


# =========================
# 🚀 RUN
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buttons))

print("💀 Doom AI Pro v5 Running...")
app.run_polling()
