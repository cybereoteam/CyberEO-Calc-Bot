import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

TOKEN = os.environ.get('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "স্বাগতম! বয়স জানতে লিখুন: `/age YYYY-MM-DD` \n"
        "যেমন: `/age 2005-08-15`"
    )

async def age_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        birth_date_str = context.args[0]
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        today = datetime.today().date()
        
        # নিখুঁত বয়স হিসাব (বছর, মাস, দিন)
        diff = relativedelta(today, birth_date)
        
        response = (
            f"📊 আপনার বর্তমান বয়স:\n"
            f"━━━━━━━━━━━━━━\n"
            f"📅 {diff.years} বছর, {diff.months} মাস, {diff.days} দিন"
        )
        await update.message.reply_text(response)
    except (IndexError, ValueError):
        await update.message.reply_text("সঠিকভাবে লিখুন: `/age বছর-মাস-দিন` (উদা: `/age 2000-12-31`)।")

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        allowed = "0123456789+-*/(). "
        if all(c in allowed for c in text):
            result = eval(text)
            await update.message.reply_text(f"ফলাফল: {result}")
    except:
        pass

if __name__ == '__main__':
    keep_alive()
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('age', age_calculator))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), calculate))
    
    application.run_polling()
