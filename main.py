from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import datetime

# قاعدة بيانات بسيطة (في الذاكرة فقط، لا قاعدة بيانات خارجية)
users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {"wallet": None, "balance": 0, "last_claim": None}
    await update.message.reply_text("👋 أهلاً بك في بوت العملة!\n\nأرسل عنوان محفظتك لربطه.")

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    address = update.message.text.strip()
    if len(address) < 10:
        await update.message.reply_text("❌ العنوان غير صالح.")
        return
    if user_id not in users:
        users[user_id] = {"wallet": address, "balance": 0, "last_claim": None}
    else:
        users[user_id]["wallet"] = address
    await update.message.reply_text(f"✅ تم حفظ عنوان محفظتك:\n{address}")

async def claim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users or users[user_id]["wallet"] is None:
        await update.message.reply_text("⚠️ أولاً أرسل عنوان محفظتك.")
        return

    today = datetime.date.today()
    last_claim = users[user_id]["last_claim"]

    if last_claim == today:
        await update.message.reply_text("⏳ لقد حصلت على مكافأتك اليومية اليوم بالفعل!")
        return

    users[user_id]["balance"] += 10  # المكافأة اليومية
    users[user_id]["last_claim"] = today

    await update.message.reply_text("🎁 تم إضافة 10 عملات إلى رصيدك!")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        await update.message.reply_text("⚠️ لم تقم بالتسجيل بعد.")
        return
    balance = users[user_id]["balance"]
    wallet = users[user_id]["wallet"] or "لم يتم تسجيل محفظة بعد"
    await update.message.reply_text(f"💰 رصيدك الحالي: {balance}\n🏦 محفظتك: {wallet}")

def main():
    app = Application.builder().token("ضع هنا توكن البوت").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("claim", claim))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wallet))

    app.run_polling()

if __name__ == "__main__":
    main()
