import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = "8690867763:AAHZLpFhevbDCz5Rg8eoZjY5VVkFPGTKg8M"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_button = KeyboardButton(text="📱 مشاركة رقم الهاتف", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True)
    
    await update.message.reply_text(
        "أهلاً بك! يرجى النقر على الزر أدناه لمشاركة رقم الهاتف:",
        reply_markup=reply_markup
    )

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    phone_number = contact.phone_number
    
    await update.message.reply_text(
        f"✅ تم استلام رقم الهاتف بنجاح:\n`{phone_number}`",
        parse_mode="Markdown"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()

