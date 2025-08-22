# 🚀 راهنمای Deploy کردن بک‌اند

## 📋 خلاصه
این پروژه شامل سیستم خودکار ایجاد کاربر ادمین هنگام deploy شدن روی سرور است.

## 🔑 اطلاعات کاربر ادمین
پس از deploy شدن، یک کاربر ادمین با مشخصات زیر ایجاد می‌شود:

- **نام کاربری**: `admin`
- **رمز عبور**: `admin`
- **ایمیل**: `admin@calligraphy.com`
- **دسترسی**: تمام دسترسی‌های ادمین

## 🛠️ فایل‌های ایجاد شده

### 1. Management Command
`users/management/commands/create_admin_user.py`
- دستور Django برای ایجاد کاربر ادمین
- قابل اجرا با: `python manage.py create_admin_user`

### 2. اسکریپت Deploy
`deploy.py`
- اسکریپت Python برای اجرای خودکار در deployment
- شامل: migrations، collectstatic، ایجاد ادمین

### 3. اسکریپت Shell
`deploy.sh`
- اسکریپت bash برای deployment
- قابل اجرا در سرورهای Linux/Unix

### 4. اسکریپت Startup
`startup.py`
- اسکریپت Python که هنگام startup سرور اجرا می‌شود
- اطمینان حاصل می‌کند که کاربر ادمین وجود دارد

### 5. اسکریپت Production
`production.py`
- اسکریپت مخصوص محیط production
- شامل بررسی‌های امنیتی و health checks

## 🚀 نحوه استفاده

### روش 1: اجرای مستقیم Management Command
```bash
cd backend
python manage.py create_admin_user
```

### روش 2: اجرای اسکریپت Python
```bash
cd backend
python deploy.py
```

### روش 3: اجرای اسکریپت Shell
```bash
cd backend
chmod +x deploy.sh
./deploy.sh
```

### روش 4: اجرای اسکریپت Production
```bash
cd backend
python production.py
```

### روش 5: اجرای اسکریپت Startup
```bash
cd backend
python startup.py
```

## ⚙️ تنظیمات پیشرفته

### تغییر مشخصات ادمین
```bash
python manage.py create_admin_user \
    --username=myadmin \
    --password=mypassword \
    --email=myadmin@example.com
```

### ایجاد مجدد کاربر (حذف و ایجاد دوباره)
```bash
python manage.py create_admin_user --force
```

## 🔒 نکات امنیتی

### ⚠️ هشدار مهم
- کاربر ادمین با رمز عبور ساده `admin` ایجاد می‌شود
- **حتماً پس از اولین ورود، رمز عبور را تغییر دهید**
- در محیط production، از رمز عبور قوی استفاده کنید

### تغییر رمز عبور
1. وارد پنل ادمین شوید: `/admin/`
2. به بخش Users بروید
3. روی کاربر admin کلیک کنید
4. رمز عبور جدید را وارد کنید
5. ذخیره کنید

## 🌐 دسترسی به پنل ادمین

پس از deploy شدن:
- **URL**: `https://yourdomain.com/admin/`
- **Username**: `admin`
- **Password**: `admin`

## 🧪 تست محلی

### تست Management Command
```bash
cd backend
python manage.py create_admin_user
python manage.py runserver
```

### تست Startup Script
```bash
cd backend
python startup.py
```

### تست Production Script
```bash
cd backend
python production.py
```

سپس به `http://localhost:8000/admin/` بروید.

## 🔄 Startup Process

### WSGI/ASGI Integration
فایل‌های `wsgi.py` و `asgi.py` به‌روزرسانی شده‌اند تا:
- Startup script را هنگام startup سرور اجرا کنند
- اطمینان حاصل کنند که کاربر ادمین وجود دارد
- خطاهای startup را log کنند بدون اینکه سرور fail شود

### Automatic Admin User Creation
- هنگام startup سرور، سیستم بررسی می‌کند که آیا کاربر ادمین وجود دارد
- اگر وجود نداشته باشد، به صورت خودکار ایجاد می‌کند
- این فرآیند در background اجرا می‌شود و سرور را block نمی‌کند

## 📝 لاگ‌ها

تمام عملیات deployment در console نمایش داده می‌شود:
```
🚀 Starting deployment process...
📊 Running database migrations...
📁 Collecting static files...
👤 Creating admin user...
🔍 Checking database connection...
✅ Database connection successful
🎉 Deployment completed successfully!
```

## 🆘 عیب‌یابی

### مشکل: خطای "No module named 'users'"
**راه‌حل**: مطمئن شوید که app `users` در `INSTALLED_APPS` اضافه شده است.

### مشکل: خطای "Permission denied"
**راه‌حل**: مطمئن شوید که فایل‌ها قابل اجرا هستند:
```bash
chmod +x deploy.sh
```

### مشکل: خطای Database
**راه‌حل**: مطمئن شوید که:
- Database connection درست تنظیم شده
- Migrations اجرا شده‌اند
- User model درست تعریف شده

## 📞 پشتیبانی

در صورت بروز مشکل:
1. لاگ‌های deployment را بررسی کنید
2. مطمئن شوید که تمام dependencies نصب شده‌اند
3. Database connection را بررسی کنید
4. Django settings را بررسی کنید
