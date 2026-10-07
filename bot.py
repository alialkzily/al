import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد السجلات لمتابعة عمل البوت
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# توكن البوت الخاص بك
TOKEN = "ضع_التوكن_هنا"

# 1. أمر البدء (الخطوة الأولى): يرحب بالمستخدم ويطلب منه مشاركة الموقع
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إنشاء زر لمشاركة الموقع الجغرافي
    location_button = KeyboardButton(text="📍 مشاركة الموقع والسماح", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[location_button]], resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "أهلاً بك في الخطوة الأولى!\n"
        "للبدء والمتابعة، يرجى السماح للبوت بالوصول إلى موقعك الجغرافي عبر الضغط على الزر أدناه 👇",
        reply_markup=reply_markup
    )

# 2. الخطوة الثانية: استقبال الموقع ثم طلب تأكيد الصلاحية مجدداً أو الانتقال للخطوة التالية
async def second_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.location:
        lat = update.message.location.latitude
        lon = update.message.location.longitude
        # يمكنك حفظ الإحداثيات هنا إذا رغبت
        
        # إنشاء زر للخطوة الثانية (طلب الموقع والسماح مرة أخرى للتأكيد)
        location_button = KeyboardButton(text="📍 تأكيد مشاركة الموقع (الخطوة الثانية)", request_location=True)
        reply_markup = ReplyKeyboardMarkup([[location_button]], resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(
            f"تم استلام إحداثيات موقعك بنجاح ✅\n\n"
            "الآن أصبحت في **الخطوة الثانية**.\n"
            "يرجى الضغط على الزر أدناه لتأكيد الموقع والسماح بالمتابعة للمرحلة الأخيرة 👇",
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

# دالة ذكية للتعامل مع المواقع المرتسلة حسب التسلسل
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # نتحقق من رسالة المستخدم لنعرف في أي خطوة هو بناءً على الزر أو السياق
    text = update.message.text
    if update.message.location:
        # إذا أرسل موقعاً، نفترض أنه تفاعل مع زر الخطوة الثانية وننقله للثالثة أو نعالجها
        await third_step(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # ربط الأوامر بالدوال
    app.add_handler(CommandHandler("start", start_command))
    
    # معالجة استلام الموقع الجغرافي من الزر
    app.add_handler(MessageHandler(filters.LOCATION, second_step))

    app.run_polling()

if __name__ == "__main__":
    main()
