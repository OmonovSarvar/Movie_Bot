import sqlite3
import logging
from config import MAIN_ADMIN_ID

def create_db():
    """Ma'lumotlar bazasini yaratish"""
    conn = sqlite3.connect("videos.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS videos (
                    video_code TEXT PRIMARY KEY,
                    video_file_id TEXT NOT NULL
                 )""")
    c.execute("""CREATE TABLE IF NOT EXISTS admins (
                    admin_id INTEGER PRIMARY KEY
                 )""")
    conn.commit()
    conn.close()

def is_admin(user_id):
    """Foydalanuvchi admin ekanligini tekshirish"""
    conn = sqlite3.connect("videos.db")
    c = conn.cursor()
    c.execute("SELECT * FROM admins WHERE admin_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result is not None or user_id == MAIN_ADMIN_ID

def add_admin(user_id):
    """Yangi admin qo'shish"""
    try:
        conn = sqlite3.connect("videos.db")
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO admins (admin_id) VALUES (?)", (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logging.error(f"Admin qo'shishda xatolik: {e}")
        return False

def save_video(video_code, video_file_id):
    """Videoni ma'lumotlar bazasiga saqlash"""
    try:
        conn = sqlite3.connect("videos.db")
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO videos (video_code, video_file_id) VALUES (?, ?)",
                  (video_code, video_file_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logging.error(f"Videoni saqlashda xatolik: {e}")
        return False

def get_video(video_code):
    """Videoni kod bo'yicha topish"""
    try:
        conn = sqlite3.connect("videos.db")
        c = conn.cursor()
        c.execute("SELECT video_file_id FROM videos WHERE video_code = ?", (video_code,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        logging.error(f"Videoni izlashda xatolik: {e}")
        return None

def delete_video(video_code):
    """Videoni o'chirish"""
    try:
        conn = sqlite3.connect("videos.db")
        c = conn.cursor()
        c.execute("DELETE FROM videos WHERE video_code = ?", (video_code,))
        rows_affected = c.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0
    except Exception as e:
        logging.error(f"Videoni o'chirishda xatolik: {e}")
        return False


def remove_admin(user_id):
    """Adminni o‘chirish"""
    try:
        conn = sqlite3.connect("videos.db")
        c = conn.cursor()
        c.execute("DELETE FROM admins WHERE admin_id = ?", (user_id,))
        rows_affected = c.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0
    except Exception as e:
        logging.error(f"Adminni o‘chirishda xatolik: {e}")
        return False