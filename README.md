# Authify

Authify یک پروژه با Django برای ساخت سیستم حساب کاربری است.

### امکانات
- ساخت حساب کاربری
- ورود و خروج
- بررسی اطلاعات ثبت‌نام
- بررسی رمز عبور
- محدود کردن ورودهای ناموفق
- تست بخش حساب کاربری

### تکنولوژی‌ها
Python، Django، SQLite، HTML و CSS

### راه‌اندازی
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### اجرای تست‌ها
```bash
python manage.py test accounts
```
