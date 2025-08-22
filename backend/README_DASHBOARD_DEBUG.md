# 🔍 راهنمای عیب‌یابی Dashboard

## 📋 مشکل
صفحه داشبورد در پنل ادمین بالا نمی‌آورد و خطای 404 برای endpoint `/api/dashboard/admin/` دریافت می‌شود.

## 🛠️ راه‌حل‌های انجام شده

### 1. **اضافه کردن Test View**
- `TestDashboardView` اضافه شده که بدون authentication کار می‌کند
- Endpoint: `/api/dashboard/test/`
- برای تست اولیه و اطمینان از کارکرد dashboard app

### 2. **بهبود AdminDashboardView**
- Error handling بهتر اضافه شده
- Safe data access با try-catch blocks
- Response ساده‌تر برای debug

### 3. **Debug Script**
- فایل `debug_dashboard.py` برای تست endpoint ها
- بررسی URL patterns
- تست authentication
- بررسی models

## 🧪 تست و عیب‌یابی

### **مرحله 1: تست Test Endpoint**
```bash
cd backend
python debug_dashboard.py
```

### **مرحله 2: تست مستقیم Endpoint**
```bash
# Test endpoint بدون authentication
curl https://calligraphybackend.onrender.com/api/dashboard/test/

# Test admin endpoint بدون authentication
curl https://calligraphybackend.onrender.com/api/dashboard/admin/
```

### **مرحله 3: بررسی URL Patterns**
```bash
cd backend
python manage.py shell
```

```python
from django.urls import get_resolver
resolver = get_resolver()

# بررسی تمام URL ها
for pattern in resolver.url_patterns:
    print(pattern)
```

## 🔍 بررسی مشکلات احتمالی

### **1. URL Configuration**
- ✅ `dashboard.urls` در `core/urls.py` include شده
- ✅ Pattern `admin/` در `dashboard/urls.py` تعریف شده
- ✅ View `AdminDashboardView` در `dashboard/views.py` وجود دارد

### **2. Authentication**
- ✅ Permission classes تنظیم شده‌اند
- ✅ User model درست import شده
- ✅ Error handling اضافه شده

### **3. Models**
- ✅ `User` model از Django
- ✅ `Course` model از courses app
- ✅ `Order` model از orders app

## 🚀 مراحل حل مشکل

### **مرحله 1: تست Test Endpoint**
ابتدا endpoint `/api/dashboard/test/` را تست کنید تا مطمئن شوید dashboard app کار می‌کند.

### **مرحله 2: بررسی Authentication**
اگر test endpoint کار کرد، مشکل از authentication است. بررسی کنید:
- User login شده است
- Token معتبر است
- User admin privileges دارد

### **مرحله 3: بررسی Models**
اگر authentication درست است، مشکل از models است. بررسی کنید:
- Database tables وجود دارند
- Models درست تعریف شده‌اند
- Migrations اجرا شده‌اند

### **مرحله 4: بررسی Permissions**
اگر models درست هستند، مشکل از permissions است. بررسی کنید:
- User `is_staff=True` دارد
- User `is_superuser=True` دارد
- Permission classes درست تنظیم شده‌اند

## 📝 لاگ‌ها و Debug

### **Console Logs**
تمام خطاها در console نمایش داده می‌شوند:
```
Dashboard error: [error message]
Error processing orders: [error message]
Error processing courses: [error message]
```

### **Response Headers**
در browser developer tools بررسی کنید:
- Status code
- Response headers
- Error messages

### **Network Tab**
در Network tab بررسی کنید:
- Request URL
- Request method
- Response status
- Response body

## 🔧 تنظیمات موقت

### **1. حذف Authentication (برای تست)**
```python
class AdminDashboardView(APIView):
    permission_classes = []  # No permissions required
```

### **2. ساده‌سازی Response**
```python
def get(self, request):
    return Response({
        'message': 'Admin Dashboard is working!',
        'status': 'success'
    })
```

### **3. اضافه کردن Debug Info**
```python
def get(self, request):
    print(f"Request user: {request.user}")
    print(f"User is staff: {request.user.is_staff}")
    print(f"User is superuser: {request.user.is_superuser}")
    # ... rest of the code
```

## 📞 پشتیبانی

### **در صورت بروز مشکل:**
1. فایل `debug_dashboard.py` را اجرا کنید
2. Console logs را بررسی کنید
3. Browser developer tools را بررسی کنید
4. Network requests را بررسی کنید
5. Django server logs را بررسی کنید

### **اطلاعات مورد نیاز:**
- Error message کامل
- Status code
- Response body
- User authentication status
- Django server logs

## 🎯 نتیجه مورد انتظار

پس از حل مشکل:
- ✅ Endpoint `/api/dashboard/admin/` کار می‌کند
- ✅ Response شامل اطلاعات dashboard است
- ✅ Authentication درست کار می‌کند
- ✅ Models درست کار می‌کنند
- ✅ صفحه داشبورد در frontend نمایش داده می‌شود
