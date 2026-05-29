#!/usr/bin/env python3
"""
🌐 Instagram Bot Pro - Flask Server
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import threading
import time
import random
import json
import os

app = Flask(__name__)
CORS(app)

# =======================
# 📂 إدارة البيانات
# =======================

CONFIG_FILE = "config.json"

def save_config(username, password, target_username=None, wait_time=900):
    config = {
        "username": username, 
        "password": password,
        "target": target_username,
        "wait_time": wait_time
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def delete_config():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)

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
# 🤖 بوت إنستغرام
# =======================

class InstagramBotWeb:
    def __init__(self):
        self.bot = None
        self.is_running = False
        self.logs = []
        self.processed_posts = set()
        self.profile_data = None
        self.media_data = []
        self.stories_data = []
        self.login_status = "closed"
    
    def login(self, username, password):
        try:
            from instabot import Bot
            self.bot = Bot()
            self.bot.login(username=username, password=password)
            time.sleep(3)
            
            if self.bot.api.is_logged_in():
                self.login_status = "logged_in"
                self.logs.append("✅ تم تسجيل الدخول بنجاح!")
                return True
            else:
                self.logs.append("❌ فشل تسجيل الدخول")
                return False
                
        except Exception as e:
            self.logs.append(f"❌ خطأ: {str(e)}")
            return False
    
    def logout(self):
        if self.bot:
            try:
                self.bot.logout()
                self.logs.append("✅ تم تسجيل الخروج")
                self.login_status = "closed"
            except:
                pass
    
    def get_profile_info(self, username):
        try:
            if not username:
                username = self.bot.username
            
            user_id = self.bot.get_user_id_from_username(username)
            if not user_id:
                return None
            
            profile_info = self.bot.get_user_info(user_id)
            
            if profile_info:
                self.profile_data = {
                    "username": profile_info.get('username', ''),
                    "full_name": profile_info.get('full_name', ''),
                    "bio": profile_info.get('biography', ''),
                    "followers": profile_info.get('follower_count', 0),
                    "following": profile_info.get('following_count', 0),
                    "posts": profile_info.get('media_count', 0),
                    "is_private": profile_info.get('is_private', False),
                    "is_verified": profile_info.get('is_verified', False),
                    "profile_pic_url": profile_info.get('profile_pic_url_hd', profile_info.get('profile_pic_url', '')),
                    "external_url": profile_info.get('external_url', '')
                }
                return self.profile_data
            
        except Exception as e:
            self.logs.append(f"❌ خطأ في جلب المعلومات: {str(e)}")
            return None
    
    def get_user_medias(self, username, amount=12):
        try:
            if not username:
                username = self.bot.username
            
            user_id = self.bot.get_user_id_from_username(username)
            if not user_id:
                return []
            
            medias = self.bot.get_user_medias(user_id, amount=amount)
            self.media_data = []
            
            for media_id in medias:
                try:
                    media_info = self.bot.get_media_info(media_id)
                    if media_info and len(media_info) > 0:
                        m = media_info[0]
                        
                        media_data = {
                            "id": m.get('id', ''),
                            "code": m.get('code', ''),
                            "type": m.get('media_type', 'image'),
                            "url": m.get('image_versions2', {}).get('candidates', [{}])[0].get('url', ''),
                            "thumbnail": m.get('image_versions2', {}).get('candidates', [{}])[-1].get('url', ''),
                            "likes": m.get('like_count', 0),
                            "comments": m.get('comment_count', 0),
                            "caption": m.get('caption', {}).get('text', '') if m.get('caption') else '',
                            "created_at": m.get('creation_timestamp', 0),
                            "link": f"https://www.instagram.com/p/{m.get('code', '')}/"
                        }
                        self.media_data.append(media_data)
                        
                except:
                    continue
            
            return self.media_data
            
        except Exception as e:
            self.logs.append(f"❌ خطأ في جلب المنشورات: {str(e)}")
            return []
    
    def get_stories(self, username):
        try:
            if not username:
                username = self.bot.username
            
            user_id = self.bot.get_user_id_from_username(username)
            if not user_id:
                return []
            
            stories = self.bot.get_user_stories(user_id)
            self.stories_data = []
            
            for story in stories:
                story_data = {
                    "id": story.get('id', ''),
                    "type": story.get('media_type', 'image'),
                    "url": story.get('image_versions2', {}).get('candidates', [{}])[0].get('url', ''),
                    "created_at": story.get('creation_timestamp', 0)
                }
                self.stories_data.append(story_data)
            
            return self.stories_data
            
        except Exception as e:
            self.logs.append(f"❌ خطأ في جلب الستوري: {str(e)}")
            return []
    
    def like(self, media_id):
        try:
            self.bot.like(media_id)
            self.logs.append(f"👍 لايك")
        except Exception as e:
            self.logs.append(f"❌ خطأ في اللايك: {str(e)}")
    
    def comment(self, media_id, text):
        try:
            self.bot.comment(media_id, text)
            self.logs.append(f"💬 تعليق: {text}")
        except Exception as e:
            self.logs.append(f"❌ خطأ في التعليق: {str(e)}")
    
    def run(self, target_username, wait_time):
        self.is_running = True
        self.logs.append(f"🚀 بدء البوت لمراقبة @{target_username}")
        
        while self.is_running:
            try:
                user_id = self.bot.get_user_id_from_username(target_username)
                
                if not user_id:
                    self.logs.append("❌ لم يتم العثور على المستخدم")
                    time.sleep(wait_time)
                    continue
                
                medias = self.bot.get_user_medias(user_id, amount=10)
                
                new_posts = []
                for media in medias:
                    if media not in self.processed_posts:
                        new_posts.append(media)
                        self.processed_posts.add(media)
                
                if new_posts:
                    for media in new_posts[:3]:
                        self.like(media)
                        time.sleep(2)
                        
                        comment = random.choice(COMMENTS)
                        self.comment(media, comment)
                        time.sleep(3)
                
                if not new_posts:
                    self.logs.append(f"⏰ انتظار... ({wait_time//60} دقيقة)")
                    
            except Exception as e:
                self.logs.append(f"❌ خطأ: {str(e)}")
            
            time.sleep(wait_time)
    
    def stop(self):
        self.is_running = False
        self.logs.append("⏹️ تم إيقاف البوت")

# إنشاء مثيل واحد
instagram_bot = InstagramBotWeb()

# =======================
# 🌐 مسارات الموقع
# =======================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if instagram_bot.login(username, password):
        save_config(username, password)
        return jsonify({"success": True, "message": "✅ تم تسجيل الدخول!"})
    else:
        return jsonify({"success": False, "message": "❌ فشل تسجيل الدخول"})

@app.route("/api/profile", methods=["GET"])
def get_profile():
    username = request.args.get("username")
    
    if instagram_bot.bot is None:
        return jsonify({"success": False, "message": "❌ سجّل دخول أولاً"})
    
    try:
        if not instagram_bot.bot.api.is_logged_in():
            return jsonify({"success": False, "message": "❌ سجّل دخول أولاً"})
    except:
        return jsonify({"success": False, "message": "❌ خطأ في الاتصال"})
    
    info = instagram_bot.get_profile_info(username)
    
    if info:
        return jsonify({"success": True, "profile": info})
    else:
        return jsonify({"success": False, "message": "❌ لم يتم العثور"})

@app.route("/api/media", methods=["GET"])
def get_media():
    username = request.args.get("username")
    amount = int(request.args.get("amount", 12))
    
    if instagram_bot.bot is None:
        return jsonify({"success": False, "message": "❌ سجّل دخول أولاً"})
    
    medias = instagram_bot.get_user_medias(username, amount)
    
    if medias:
        return jsonify({"success": True, "media": medias})
    else:
        return jsonify({"success": False, "message": "❌ لا توجد منشورات"})

@app.route("/api/stories", methods=["GET"])
def get_stories():
    username = request.args.get("username")
    
    if instagram_bot.bot is None:
        return jsonify({"success": False, "message": "❌ سجّل دخول أولاً"})
    
    stories = instagram_bot.get_stories(username)
    return jsonify({"success": True, "stories": stories})

@app.route("/api/start", methods=["POST"])
def start_bot():
    config = load_config()
    data = request.json or {}
    
    target = data.get("target")
    wait_time = int(data.get("wait_time", 900))
    
    if not target:
        return jsonify({"success": False, "message": "❌ أدخل اسم المستخدم"})
    
    if instagram_bot.bot is None:
        return jsonify({"success": False, "message": "❌ سجّل دخول أولاً"})
    
    try:
        if not instagram_bot.bot.api.is_logged_in():
            return jsonify({"success": False, "message": "❌ سجّل دخول أولاً"})
    except:
        return jsonify({"success": False, "message": "❌ خطأ"})
    
    save_config(config["username"], config["password"], target, wait_time)
    
    thread = threading.Thread(
        target=instagram_bot.run,
        args=(target, wait_time)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({"success": True, "message": f"🚀 جاري العمل على @{target}"})

@app.route("/api/stop", methods=["POST"])
def stop_bot():
    instagram_bot.stop()
    return jsonify({"success": True, "message": "⏹️ تم الإيقاف"})

@app.route("/api/logs")
def get_logs():
    return jsonify({"logs": instagram_bot.logs[-20:]})

@app.route("/api/status")
def get_status():
    logged_in = False
    try:
        logged_in = instagram_bot.bot.api.is_logged_in() if instagram_bot.bot else False
    except:
        logged_in = False
    
    return jsonify({
        "running": instagram_bot.is_running,
        "logged_in": logged_in
    })

@app.route("/api/logout", methods=["POST"])
def logout():
    instagram_bot.logout()
    delete_config()
    return jsonify({"success": True})

# =======================
# ▶️ تشغيل
# =======================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
