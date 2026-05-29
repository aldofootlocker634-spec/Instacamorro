#!/usr/bin/env python3
"""
🌐 Instagram Bot - Selenium Version
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import threading
import time
import random
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
CORS(app)

# =======================
# 📂 إدارة البيانات
# =======================

CONFIG_FILE = "config.json"

def save_config(username, password, target=None, wait_time=900):
    config = {
        "username": username, 
        "password": password,
        "target": target,
        "wait_time": wait_time
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# =======================
# 💬 التعليقات
# =======================

COMMENTS = [
    "هالشي خطييييير 😂🔥",
    "والله عقلتني 😂",
    "ماشاء الله تبارك الله 🙌",
    "جميل جداً 🔥",
    "عملاقة 🇸🇦💪",
    "Keep it up! 💪",
    "ننتظر المزيد 🔜",
    "أنت مبدع ✨",
    "very nice 🔥",
    "love it 😍",
    "مذهل 👌🔥",
    "awesome 💯",
]

# =======================
# 🤖 Selenium Driver
# =======================

class InstaDriver:
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
        
    def start_driver(self):
        """بدء المتصفح"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS_14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
        
    def login(self, username, password):
        """تسجيل دخول"""
        try:
            if not self.driver:
                self.start_driver()
            
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            # إدخال اسم المستخدم
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.clear()
            username_input.send_keys(username)
            time.sleep(1)
            
            # إدخال كلمة المرور
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys(password)
            time.sleep(1)
            
            # الضغط على زر تسجيل الدخول
            login_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_btn.click()
            
            # انتظار التحميل
            time.sleep(5)
            
            # التحقق من تسجيل الدخول
            if "instagram.com" in self.driver.current_url and "accounts/login" not in self.driver.current_url:
                self.is_logged_in = True
                return True, "✅ تم تسجيل الدخول!"
            else:
                return False, "❌ فشل تسجيل الدخول - تحقق من البيانات"
                
        except Exception as e:
            return False, f"❌ خطأ: {str(e)}"
    
    def get_profile(self, username):
        """جلب معلومات الحساب"""
        try:
            self.driver.get(f"https://www.instagram.com/{username}/")
            time.sleep(3)
            
            # جلب الاسم الكامل
            try:
                full_name = self.driver.find_element(By.XPATH, "//h1[@class='_aak1']").text
            except:
                full_name = ""
            
            # جلب البايو
            try:
                bio = self.driver.find_element(By.XPATH, "//span[@class='_aacl']").text
            except:
                bio = ""
            
            # جلب عدد المتابعين
            try:
                followers = self.driver.find_element(By.XPATH, "//a[contains(@href, 'followers')]//span").text
            except:
                followers = "0"
            
            # جلب عدد المتابعة
            try:
                following = self.driver.find_element(By.XPATH, "//a[contains(@href, 'following')]//span").text
            except:
                following = "0"
            
            # جلب عدد المنشورات
            try:
                posts = self.driver.find_element(By.XPATH, "//a[contains(@href, 'posts')]//span").text
            except:
                posts = "0"
            
            # جلب صورة الملف الشخصي
            try:
                img = self.driver.find_element(By.XPATH, "//img[@class='_aapq']").get_attribute('src')
            except:
                img = ""
            
            return {
                "username": username,
                "full_name": full_name,
                "bio": bio,
                "followers": followers,
                "following": following,
                "posts": posts,
                "profile_pic": img
            }
            
        except Exception as e:
            return None
    
    def get_posts(self, username, amount=12):
        """جلب المنشورات"""
        try:
            self.driver.get(f"https://www.instagram.com/{username}/")
            time.sleep(3)
            
            # التمرير لجلب المنشورات
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            
            # جلب الروابط
            posts = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
            
            post_data = []
            for post in posts[:amount]:
                link = post.get_attribute('href')
                post_data.append({
                    "link": link,
                    "code": link.split('/p/')[-1].replace('/', '')
                })
            
            return post_data
            
        except Exception as e:
            return []
    
    def like_post(self, post_link):
        """عمل لايك"""
        try:
            self.driver.get(post_link)
            time.sleep(2)
            
            # البحث عن زر اللايك
            like_btn = self.driver.find_element(By.XPATH, "//article//section//span/button")
            like_btn.click()
            return True
            
        except:
            return False
    
    def comment_post(self, post_link, text):
        """تعليق"""
        try:
            self.driver.get(post_link)
            time.sleep(2)
            
            # البحث عن حقل التعليق
            comment_box = self.driver.find_element(By.XPATH, "//form//textarea")
            comment_box.send_keys(text)
            time.sleep(1)
            
            # الضغط على إرسال
            submit_btn = self.driver.find_element(By.XPATH, "//form//button[@type='submit']")
            submit_btn.click()
            return True
            
        except:
            return False
    
    def quit(self):
        """إغلاق المتصفح"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.is_logged_in = False

# =======================
# 🔧 مثيل واحد
# =======================

insta_driver = InstaDriver()

# =======================
# 🧵 خيوط العمل
# =======================

logs = []

def run_bot(target_username, wait_time):
    """تشغيل البوت"""
    global logs
    
    try:
        while True:
            logs.append(f"🔍 جاري البحث عن @{target_username}")
            
            # جلب المنشورات الجديدة
            posts = insta_driver.get_posts(target_username, amount=10)
            
            if posts:
                # اللايك والتعليق على أول 3 منشورات
                for post in posts[:3]:
                    insta_driver.like_post(post['link'])
                    time.sleep(2)
                    
                    comment = random.choice(COMMENTS)
                    insta_driver.comment_post(post['link'], comment)
                    time.sleep(3)
                    
                    logs.append(f"✅ لايك وتعليق على {post['code']}")
            else:
                logs.append(f"⏰ لا توجد منشورات جديدة")
            
            logs.append(f"😴 انتظار {wait_time//60} دقيقة...")
            time.sleep(wait_time)
            
    except Exception as e:
        logs.append(f"❌ خطأ: {str(e)}")

bot_thread = None

# =======================
# 🌐 المسارات
# =======================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    success, message = insta_driver.login(username, password)
    
    if success:
        save_config(username, password)
        return jsonify({"success": True, "message": message})
    else:
        return jsonify({"success": False, "message": message})

@app.route("/api/profile", methods=["GET"])
def get_profile():
    username = request.args.get("username", "")
    
    if not insta_driver.is_logged_in:
        return jsonify({"success": False, "message": "❌ سجّل دخول أولاً"})
    
    profile = insta_driver.get_profile(username)
    
    if profile:
        return jsonify({"success": True, "profile": profile})
    else:
        return jsonify({"success": False, "message": "❌ لم يتم العثور"})

@app.route("/api/media", methods=["GET"])
def get_media():
    username = request.args.get("username", "")
    amount = int(request.args.get("amount", 12))
    
    if not insta_driver.is_logged_in:
        return jsonify({"success": False, "message": "❌ سجّل دخول أولاً"})
    
    posts = insta_driver.get_posts(username, amount)
    return jsonify({"success": True, "media": posts})

@app.route("/api/start", methods=["POST"])
def start_bot():
    global bot_thread, logs
    
    data = request.json or {}
    target = data.get("target", "")
    wait_time = int(data.get("wait_time", 900))
    
    if not target:
        return jsonify({"success": False, "message": "❌ أدخل اسم المستخدم"})
    
    if not insta_driver.is_logged_in:
        return jsonify({"success": False, "message": "❌ سجّل دخول أولاً"})
    
    config = load_config()
    if config:
        save_config(config["username"], config["password"], target, wait_time)
    
    bot_thread = threading.Thread(target=run_bot, args=(target, wait_time))
    bot_thread.daemon = True
    bot_thread.start()
    
    return jsonify({"success": True, "message": f"🚀 جاري العمل على @{target}"})

@app.route("/api/stop", methods=["POST"])
def stop_bot():
    global logs
    logs.append("⏹️ تم إيقاف البوت")
    return jsonify({"success": True, "message": "⏹️ تم الإيقاف"})

@app.route("/api/logs")
def get_logs():
    return jsonify({"logs": logs[-20:]})

@app.route("/api/status")
def get_status():
    return jsonify({
        "running": bot_thread.is_alive() if bot_thread else False,
        "logged_in": insta_driver.is_logged_in
    })

@app.route("/api/logout", methods=["POST"])
def logout():
    insta_driver.quit()
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    return jsonify({"success": True})

# =======================
# ▶️ تشغيل
# =======================

if __name__ == "__main__":
    print("🚀 Starting Instagram Bot...")
    app.run(debug=True, host="0.0.0.0", port=5000)
