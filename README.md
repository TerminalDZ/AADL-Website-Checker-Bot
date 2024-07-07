# AADL Website Checker Bot

This program checks the status of the AADL website and sends alerts via Telegram.

هذا البرنامج يقوم بالتحقق من حالة موقع AADL وإرسال تنبيهات عبر Telegram.

[فيديو شرح | Explanation video ](https://www.tiktok.com/@terminal.dz/video/7388716489731362053)

## Installation / التثبيت

### On Windows / على ويندوز:

1. Install Python from the [official website](https://www.python.org/downloads/windows/).
   قم بتثبيت Python من [الموقع الرسمي](https://www.python.org/downloads/windows/).

2. Install required packages using pip:
   قم بتثبيت الحزم المطلوبة باستخدام pip:

    ```
    pip install -r requirements.txt
    ```

3. Install [Google Chrome](https://www.google.com/chrome/) (required for Selenium WebDriver).
   قم بتثبيت Google Chrome (مطلوب لـ Selenium WebDriver).

### On Linux / على لينكس:

1. Install Python using your distribution's package manager. On Ubuntu, you can use:
   قم بتثبيت Python باستخدام مدير الحزم الخاص بتوزيعتك. على Ubuntu، يمكنك استخدام الأمر:

    ```
    sudo apt-get install python3
    ```

2. Install required packages using pip:
   قم بتثبيت الحزم المطلوبة باستخدام pip:

    ```
    pip install -r requirements.txt
    ```

3. Install Google Chrome using your distribution's package manager, or download it from the [official website](https://www.google.com/chrome/).
   قم بتثبيت Google Chrome باستخدام مدير الحزم الخاص بتوزيعتك، أو قم بتنزيله من [الموقع الرسمي](https://www.google.com/chrome/).

## Creating a Telegram Bot / إنشاء بوت على Telegram

1. Open Telegram and search for the BotFather.
   افتح Telegram وابحث عن BotFather.

2. Start a chat with the BotFather and send the command:
   ابدأ محادثة مع BotFather وأرسل الأمر:

    ```
    /newbot
    ```

3. Follow the instructions to set the bot's name and username. You will receive a token upon successful creation.
   اتبع التعليمات لتعيين اسم البوت واسم المستخدم. ستحصل على رمز (TOKEN) بعد الإنشاء بنجاح.

4. Save the token, which will be used as TELEGRAM_TOKEN in your script.
   احفظ الرمز (TOKEN) الذي سيتم استخدامه كـ TELEGRAM_TOKEN في البرنامج الخاص بك.

## Usage / الاستخدام

1. Modify the code to add your bot token and chat ID.
   قم بتعديل الكود لإضافة رمز البوت الخاص بك ومعرف الدردشة.

2. Run the program using Python:
   قم بتشغيل البرنامج باستخدام Python:

    ```
    python python-telegram-bot.py
    ```

## Available Commands / الأوامر المتاحة

- `/start` - Start monitoring / بدء المراقبة
- `/stop` - Stop monitoring / إيقاف المراقبة
- `/menu` - Display settings menu / عرض قائمة الإعدادات
- `/setinterval` - Set the interval for checking / تعيين الفاصل الزمني للفحص
- `/seturl` - Set the URL address for the website / تعيين عنوان URL للموقع
- `/help` - Display this message / عرض هذه الرسالة
