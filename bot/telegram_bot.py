import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from django.conf import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Ro'yxatdan o'tish", callback_data='register')],
        [InlineKeyboardButton("Kirish", callback_data='login')],
        [InlineKeyboardButton("Yordam", callback_data='help')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        f"Salom, {user.first_name}! 👋\n\n"
        "🎓 **Lavozim O'quv Platformasi** ga xush kelibsiz!\n\n"
        "Bu yerda siz o'z lavozimingiz bo'yicha o'quv dasturlarini "
        "o'tashingiz, test topshirishingiz va sertifikat olishingiz mumkin.\n\n"
        "Quyidagi tugmalardan birini tanlang:"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'register':
        await query.edit_message_text(
            "📝 Ro'yxatdan o'tish uchun telefon raqamingizni kiriting:\n\n"
            "Format: +998XXXXXXXXX"
        )
        context.user_data['awaiting'] = 'register_phone'

    elif query.data == 'login':
        await query.edit_message_text(
            "🔑 Kirish uchun telefon raqamingizni kiriting:"
        )
        context.user_data['awaiting'] = 'login_phone'

    elif query.data == 'help':
        help_text = (
            "📚 **Yordam**\n\n"
            "• /start - Botni qayta ishga tushirish\n"
            "• /profile - Profilingizni ko'rish\n"
            "• /courses - O'quv dasturlaringiz\n"
            "• /progress - Progressingiz\n"
            "• /help - Yordam\n\n"
            "Savollaringiz bo'lsa, administratorga murojaat qiling."
        )
        await query.edit_message_text(help_text, parse_mode='Markdown')


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"👤 **Profil**\n\n"
        f"Ism: {user.first_name} {user.last_name or ''}\n"
        f"Username: @{user.username or 'yo\'q'}\n"
        f"Telegram ID: `{user.id}`"
    )
    await update.message.reply_text(text, parse_mode='Markdown')


async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 **O'quv dasturlaringiz**\n\n"
        "Hozircha sizga hech qanday lavozim biriktirilmagan.\n"
        "Admin panel orqali lavozim biriktirilgandan keyin bu yerda ko'rinadi.",
        parse_mode='Markdown'
    )


async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 **Progressingiz**\n\n"
        "Hozircha progress mavjud emas.\n"
        "Darslarni o'tashni boshlang!",
        parse_mode='Markdown'
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "❓ **Yordam**\n\n"
        "Bu bot orqali siz:\n"
        "• O'quv dasturlarini ko'rishingiz\n"
        "• Darslarni o'tashingiz\n"
        "• Test topshirishingiz\n"
        "• Progressingizni kuzatishingiz mumkin\n\n"
        "Buyruqlar:\n"
        "/start - Bosh sahifa\n"
        "/profile - Profil\n"
        "/courses - Kurslar\n"
        "/progress - Progress"
    )
    await update.message.reply_text(text, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    awaiting = context.user_data.get('awaiting')

    if awaiting == 'register_phone':
        phone = update.message.text
        context.user_data['register_phone'] = phone
        context.user_data['awaiting'] = 'register_name'
        await update.message.reply_text("Ismingizni kiriting:")

    elif awaiting == 'register_name':
        name = update.message.text
        context.user_data['register_name'] = name
        context.user_data['awaiting'] = 'register_password'
        await update.message.reply_text("Parol yarating:")

    elif awaiting == 'register_password':
        from accounts.models import User
        phone = context.user_data.get('register_phone')
        name = context.user_data.get('register_name')
        password = update.message.text
        telegram_id = str(update.effective_user.id)

        if not User.objects.filter(telegram_id=telegram_id).exists():
            user = User.objects.create_user(
                username=phone,
                phone_number=phone,
                full_name=name,
                password=password,
                telegram_id=telegram_id,
                role='employee'
            )
            await update.message.reply_text(
                f"✅ Ro'yxatdan muvaffaqiyatli o'tdingiz!\n\n"
                f"Ism: {name}\n"
                f"Telefon: {phone}"
            )
        else:
            await update.message.reply_text("Siz allaqachon ro'yxatdan o'tgansiz!")

        context.user_data.clear()

    elif awaiting == 'login_phone':
        phone = update.message.text
        context.user_data['login_phone'] = phone
        context.user_data['awaiting'] = 'login_password'
        await update.message.reply_text("Parolni kiriting:")

    elif awaiting == 'login_password':
        from accounts.models import User
        from django.contrib.auth import authenticate
        phone = context.user_data.get('login_phone')
        password = update.message.text
        telegram_id = str(update.effective_user.id)

        user = User.objects.filter(phone_number=phone).first()
        if user:
            user.telegram_id = telegram_id
            user.save()
            await update.message.reply_text(
                f"✅ Tizimga muvaffaqiyatli kirdingiz!\n\n"
                f"Xush kelibsiz, {user.full_name}!"
            )
        else:
            await update.message.reply_text("Telefon raqami yoki parol noto'g'ri!")

        context.user_data.clear()


def run_bot():
    token = settings.TELEGRAM_BOT_TOKEN
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('profile', profile))
    application.add_handler(CommandHandler('courses', courses))
    application.add_handler(CommandHandler('progress', progress))
    application.add_handler(CommandHandler('help', help_cmd))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Telegram bot ishga tushdi!")
    application.run_polling()
