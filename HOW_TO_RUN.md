# 🛠 دليل تشغيل مشروع FindMe Backend

هذا الدليل مخصص للمطورين لتجهيز بيئة العمل وتشغيل المشروع بسرعة.

## 1️⃣ المتطلبات الأساسية
- **Python:** نسخة 3.8 أو 3.9 أو 3.10 (يفضل 3.10).
- **MongoDB:** يجب أن يكون لديك قاعدة بيانات MongoDB تعمل (محلياً أو على Atlas).

## 2️⃣ خطوات التجهيز (Setup)

1. **إنشاء البيئة الوهمية (Virtual Environment):**
   ```powershell
   python -m venv venv
   ```

2. **تفعيل البيئة الوهمية:**
   - **Windows:** `.\venv\Scripts\activate`
   - **Mac/Linux:** `source venv/bin/activate`

3. **تثبيت المكتبات المطلوبة:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **إعداد متغيرات البيئة:**
   - قم بنسخ ملف `.env.example` إلى ملف جديد باسم `.env`.
   - قم بتحديث قيم `MONGO_URI` و `SECRET_KEY` في ملف `.env`.

## 3️⃣ تشغيل المشروع

1. **تجهيز قاعدة البيانات:**
   ```powershell
   python manage.py makemigrations api
   python manage.py migrate
   ```

2. **بدء السيرفر:**
   ```powershell
   python manage.py runserver
   ```

## ⚠️ ملاحظات هامة
- **أول عملية بحث:** عند تشغيل ميزة البحث بالصور لأول مرة، قد يتأخر السيرفر قليلاً لتحميل موديلات الذكاء الاصطناعي (Weights) وتكوين ملفات الـ Cache.
- **الاتصال من الموبايل:** إذا كنت ستجرب تطبيق Flutter من موبايل حقيقي، تأكد من كتابة الـ IP الخاص بجهاز الكمبيوتر في كود Flutter بدلاً من `localhost` (مثال: `http://192.168.1.5:8000`).

---
*تم إعداد هذا الدليل بواسطة Antigravity AI.*
