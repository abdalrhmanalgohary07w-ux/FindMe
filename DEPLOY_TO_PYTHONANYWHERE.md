# دليل الرفع على PythonAnywhere (Deployment Guide)

لقد قمت بتجهيز الإعدادات الأساسية في `settings.py`. اتبع الخطوات التالية بدقة لرفع المشروع وتشغيله:

## 1. رفع الملفات
*   قم بضغط ملفات المشروع (باستثناء المجلدات مثل `__pycache__` و `venv` إذا كانت موجودة).
*   ارفع الملف المضغوط إلى PythonAnywhere وقم بفك الضغط في المسار الرئيسي `/home/yourusername/`.

## 2. إنشاء بيئة وهمية (Virtual Environment)
افتح الـ Console في PythonAnywhere ونفذ الأوامر التالية:
```bash
mkvirtualenv --python=/usr/bin/python3.10 findme-env
pip install -r requirements.txt
```
*ملاحظة: تثبيت TensorFlow قد يستغرق وقتاً طويلاً جداً، تأكد من وجود مساحة كافية.*

## 3. إعدادات الموقع (Web Tab)
في صفحة **Web** في PythonAnywhere:
1.  **Source code:** `/home/yourusername/Backend`
2.  **Working directory:** `/home/yourusername/Backend`
3.  **Virtualenv:** `/home/yourusername/.virtualenvs/findme-env`
4.  **Static Files:**
    *   URL: `/static/` -> Path: `/home/yourusername/Backend/staticfiles`
    *   URL: `/media/` -> Path: `/home/yourusername/Backend/media`

## 4. ملف WSGI
في صفحة Web، اضغط على رابط "WSGI configuration file" وقم بتعديل المحتوى ليكون كالتالي:
```python
import os
import sys

path = '/home/yourusername/Backend'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'findme_backend.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 5. مشكلة الـ AI و DeepFace (هام جداً)
PythonAnywhere (الخطة المجانية) يمنع تحميل ملفات الموديلات تلقائياً. الموديلات التي نستخدمها هي:
*   **Facenet512**
*   **RetinaFace**

يجب عليك تحميل هذه الملفات يدوياً ووضعها في مجلد `.deepface/weights` داخل الهوم دايركتوري الخاص بك.

### المسارات المطلوبة:
```text
/home/yourusername/.deepface/weights/facenet512_weights.h5
/home/yourusername/.deepface/weights/retinaface.h5
```

## 6. الخطوات النهائية (في الكونسول)
```bash
python manage.py collectstatic --noinput
python manage.py migrate
```

---
**تنبيه:** إذا كانت المساحة التخزينية لا تكفي (512MB)، قد تضطر للترقية لخطة مدفوعة أو استخدام سيرفر آخر مثل Google Cloud أو AWS لأن TensorFlow وحده يستهلك مساحة كبيرة.
