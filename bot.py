import os
import logging
from datetime import datetime
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Flask Server for Keep Alive
app = Flask('')
@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# টোকেন সংগ্রহ (Render Environment Variable থেকে)
TOKEN = os.environ.get('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "স্বাগতম! আমি Cybereo Team-এর একটি মাল্টি-ফাংশন বট।\n\n"
        "🔢 **ক্যালকুলেটর:** সরাসরি অংক পাঠান (যেমন: 10 + 20)\n"
        "🎂 **বয়স গণনা:** লিখুন `/age YYYY-MM-DD` (যেমন: `/age 2000-03-27`)\n"
    )
    await update.message.reply_text(welcome_msg)

# বয়স গণনার ফাংশন
async def age_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        birth_date_str = context.args[0]
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
        today = datetime.today()
        
        age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        await update.message.reply_text(f"আপনার বর্তমান বয়স: {age_years} বছর।")
    except (IndexError, ValueError):
        await update.message.reply_text("ভুল ফরম্যাট! এভাবে লিখুন: `/age বছর-মাস-দিন` (উদা: `/age 1998-12-31`)।")

# ক্যালকুলেটর ফাংশন
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        # শুধুমাত্র গাণিতিক ক্যারেক্টার অ্যালাউ করা হচ্ছে নিরাপত্তার জন্য
        allowed = "0123456789+-*/(). "
        if all(c in allowed for c in text):
            result = eval(text)
            await update.message.reply_text(f"ফলাফল: {result}")
    except Exception:
        pass # সাধারণ টেক্সট হলে ইগনোর করবে

if __name__ == '__main__':
    keep_alive()
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('age', age_calculator))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), calculate))
    
    print("বটটি এখন অনলাইন...")
    application.run_polling()
