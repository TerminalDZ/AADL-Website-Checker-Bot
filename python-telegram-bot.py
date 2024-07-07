import asyncio
import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    'TELEGRAM_TOKEN': 'TELEGRAM_TOKEN',
    'URL': 'https://aadl3inscription2024.dz/AR/Inscription-desktop.php',
    'CHECK_INTERVAL': 10
}

class AADLChecker:
    def __init__(self, chat_id: str):
        self.config = DEFAULT_CONFIG.copy()
        self.config['CHAT_ID'] = chat_id
        self.bot = Bot(token=self.config['TELEGRAM_TOKEN'])
        self.driver = None
        self.is_running = False

    async def send_telegram_message(self, message: str, photo_path: str = None):
        await self.bot.send_message(chat_id=self.config['CHAT_ID'], text=message)
        if photo_path:
            with open(photo_path, 'rb') as photo:
                await self.bot.send_photo(chat_id=self.config['CHAT_ID'], photo=photo)

    def setup_driver(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def capture_screenshot(self):
        screenshot_path = 'screenshot.png'
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path

    @staticmethod
    def check_message_in_html(html: str, message: str) -> bool:
        soup = BeautifulSoup(html, 'html.parser')
        return message in soup.text

    async def check_website(self):
        try:
            self.setup_driver()
            self.driver.get(self.config['URL'])
            screenshot_path = self.capture_screenshot()
            
            response = requests.get(self.config['URL'])
            if response.status_code == 200:
                if self.check_message_in_html(response.text, 'تعذر الإتصال بالخادم حاليا ، يرجى المحاولة لاحقا'):
                    await self.send_telegram_message('تعذر الإتصال بالخادم حاليا ، يرجى المحاولة لاحقا', screenshot_path)
                else:
                    await self.send_telegram_message('الموقع يعمل! Status: 200', screenshot_path)
            else:
                await self.send_telegram_message(f'الموقع لم يعمل بعد. Status: {response.status_code}', screenshot_path)
        except requests.exceptions.RequestException as e:
            await self.send_telegram_message(f"خطأ عند محاولة الوصول إلى الموقع: {e}")
        finally:
            if self.driver:
                self.driver.quit()

    async def run(self):
        self.is_running = True
        while self.is_running:
            await self.check_website()
            for i in range(self.config['CHECK_INTERVAL'], 0, -1):
                if self.is_running:
                    await self.send_telegram_message(f"الوقت المتبقي: {i} ثواني")
                    await asyncio.sleep(1)
           

    def stop(self):
        self.is_running = False

    def set_interval(self, interval: int):
        self.config['CHECK_INTERVAL'] = interval

    def set_url(self, url: str):
        self.config['URL'] = url

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    checker = AADLChecker(str(chat_id))
    context.chat_data['checker'] = checker
    await update.message.reply_text('تم بدء المراقبة. سوف تتلقى إشعارات حول حالة الموقع.')
    asyncio.create_task(checker.run())

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'checker' in context.chat_data:
        context.chat_data['checker'].stop()
        await update.message.reply_text('تم إيقاف المراقبة.')
    else:
        await update.message.reply_text('لم يتم بدء المراقبة بعد.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    الأوامر المتاحة:
    /start - بدء المراقبة
    /stop - إيقاف المراقبة
    /menu - عرض قائمة الإعدادات
    /setinterval - تعيين الفاصل الزمني للفحص
    /seturl - تعيين عنوان URL للموقع
    /help - عرض هذه الرسالة
    """
    await update.message.reply_text(help_text)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("تعيين الفاصل الزمني", callback_data='setinterval')],
        [InlineKeyboardButton("تعيين URL", callback_data='seturl')],
        [InlineKeyboardButton("إيقاف المراقبة", callback_data='stop')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('اختر إعداداً:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'setinterval':
        await query.edit_message_text("الرجاء إدخال الفاصل الزمني الجديد بالثواني.")
        context.user_data['expect_interval'] = True
    elif query.data == 'seturl':
        await query.edit_message_text("الرجاء إدخال عنوان URL الجديد.")
        context.user_data['expect_url'] = True
    elif query.data == 'stop':
        if 'checker' in context.chat_data:
            context.chat_data['checker'].stop()
            await query.edit_message_text("تم إيقاف المراقبة.")
        else:
            await query.edit_message_text("لم يتم بدء المراقبة بعد.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('expect_interval'):
        try:
            interval = int(update.message.text)
            if 'checker' in context.chat_data:
                context.chat_data['checker'].set_interval(interval)
                await update.message.reply_text(f"تم تعيين الفاصل الزمني إلى {interval} ثانية.")
            else:
                await update.message.reply_text("لم يتم بدء المراقبة بعد.")
        except ValueError:
            await update.message.reply_text("الرجاء إدخال رقم صحيح.")
        context.user_data['expect_interval'] = False
    elif context.user_data.get('expect_url'):
        if 'checker' in context.chat_data:
            context.chat_data['checker'].set_url(update.message.text)
            await update.message.reply_text(f"تم تعيين URL إلى {update.message.text}")
        else:
            await update.message.reply_text("لم يتم بدء المراقبة بعد.")
        context.user_data['expect_url'] = False
    else:
        await update.message.reply_text('أمر غير معروف. استخدم /help للحصول على قائمة الأوامر.')

if __name__ == '__main__':
    application = ApplicationBuilder().token(DEFAULT_CONFIG['TELEGRAM_TOKEN']).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('stop', stop))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('menu', menu))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()