import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# এখানে আপনার সংগৃহীত API Token দিন
TOKEN = '8551054225:AAH-yRL5WhnGAJOV3oxVSEI84GB14KJctck'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো! আমি একটি ক্যালকুলেটর বট। আমাকে যেকোনো অংক পাঠান (যেমন: 5+5), আমি সমাধান করে দেব।")

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        # eval ফাংশন অংকটি সমাধান করে
        result = eval(text)
        await update.message.reply_text(f"ফলাফল: {result}")
    except Exception:
        await update.message.reply_text("দুঃখিত, আপনার দেওয়া অংকটি বুঝতে পারছি না। সঠিক ফরম্যাটে লিখুন (উদা: 10 * 20)।")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    calc_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), calculate)
    
    application.add_handler(start_handler)
    application.add_handler(calc_handler)
    
    print("বটটি এখন চালু আছে...")
    application.run_polling()
