# 📖 الدليل التقني الشامل لمشروع FindMe Backend

هذا الملف مُعد خصيصاً لمساعدتك في فهم كل تفصيلة في المشروع استعداداً للمناقشة. المشروع ليس مجرد "موقع" بل هو **نظم استرجاع معلومات قائمة على الملامح الحيوية (Biometric Information Retrieval System)**.

---

## 1️⃣ السيناريو التشغيلي (Operational Scenario)
كيف يعمل النظام من اللحظة التي يفتح فيها المستخدم التطبيق؟

### أ- سيناريو تسجيل شخص مفقود:
1. يرسل الموبايل بيانات الشخص (الاسم، السن، الموقع) مع **الصورة الشخصية**.
2. يستقبل **Django** الطلب ويخزن البيانات في قاعدة بيانات **MongoDB**.
3. يتم حفظ الصورة في مجلد `media/missing_persons/`.
4. الآن أصبح هذا الشخص "مرجعاً" (Reference) يمكن البحث عنه لاحقاً.

### ب- سيناريو البحث عن شخص (The AI Flow):
1. يجد مستخدم طفلاً في الشارع، فيقوم بتصويره وإرسال الصورة لنقطة النهاية `/search-by-image/`.
2. يستلم السيرفر الصورة ويحفظها مؤقتاً باسم `temp_search.jpg`.
3. يستدعي السيرفر "الخدمة الذكية" (`FaceRecognitionService`).
4. يبدأ موديل **DeepFace** في تحويل ملامح الصورة المرفوعة إلى "مصفوفة أرقام" (Embedding).
5. يقوم الموديل بمقارنة هذه الأرقام مع كل الصور المخزنة عندنا في `media/`.
6. إذا وجد تشابهاً بنسبة أعلى من 55% (Threshold)، يرجع بيانات الشخص.
7. يمسح السيرفر الصورة المؤقتة ويرسل النتائج كاملة للموبايل.

---

## 2️⃣ شرح الأكواد بالتفصيل (Code Deep Dive)

### أولاً: الموديل (Models.py) - "قلب البيانات"
هذا الملف هو المسؤول عن شكل البيانات في MongoDB.

```python
class MissingPerson(models.Model):
    # الحقول الأساسية
    full_name = models.CharField(max_length=255) # اسم الشخص
    age = models.IntegerField(null=True)         # السن (اختياري)
    gender = models.CharField(...)              # الجنس
    
    # حتة ذكية: الموقع الجغرافي
    latitude = models.DecimalField(...)          # خط العرض
    longitude = models.DecimalField(...)         # خط الطول
    
    # الصورة: أهم حقل
    image = models.ImageField(upload_to='missing_persons/') # مكان تخزين صور الـ Database
```
**للمناقشة:** قل "نستخدم `DecimalField` للإحداثيات لضمان الدقة العالية في تحديد المواقع الجغرافية".

---

### ثانياً: الخدمة الذكية (Services.py) - "المخ"
هنا يحدث السحر. استخدمنا "طبقة الخدمات" (Service Layer) لفصل كود الذكاء الاصطناعي عن كود الويب.

```python
class FaceRecognitionService:
    @staticmethod
    def find_matches(image_path):
        # نستدعي DeepFace
        results = DeepFace.find(
            img_path=image_path,       # الصورة اللي بنبحث بيها
            db_path=settings.MEDIA_ROOT, # المخزن اللي فيه كل الصور
            model_name='Facenet512',      # أقوى موديل للتعرف على الوجوه
            distance_metric='cosine'      # طريقة حساب المسافة بين الوشوش
        )
```
**للمناقشة:** قل "استخدمنا موديل `Facenet512` لأنه يوفر 512 نقطة مميزة للوجه، مما يجعله دقيقاً جداً حتى لو كانت الإضاءة ضعيفة".

---

### ثالثاً: المتحكم (Views.py) - "المنظم"
هذا هو موظف الاستقبال الذي يربط كل شيء ببعضه.

```python
class MissingPersonViewSet(viewsets.ModelViewSet):
    # خوارزميات البحث التقليدي (بالاسم أو الموقع)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['full_name', 'last_seen_location']

    @action(detail=False, methods=['post'], url_path='search-by-image')
    def search_by_image(self, request):
        # 1. استلام الصورة من REQUEST
        image_file = request.FILES.get('image')
        # 2. إرسالها للـ Service للبحث
        matched_person_ids = FaceRecognitionService.find_matches(temp_path)
        # 3. جلب بيانات الأشخاص اللي طلعوا من الـ Database
        matched_persons = MissingPerson.objects.filter(id__in=matched_person_ids)
```
**للمناقشة:** قل "استخدمنا `Action` مخصص داخل الـ `ViewSet` لإضافة ميزة البحث بالصور دون كسر معايير الـ REST API".

---

## 3️⃣ مصطلحات هامة للمناقشة (Keywords)

1.  **NoSQL (MongoDB):** قل "استخدمنا MongoDB لمرونتها في التعامل مع بيانات المفقودين التي قد تختلف تفاصيلها من حالة لأخرى".
2.  **REST Framework:** قل "بنينا الـ API باستخدام Django REST Framework لضمان سهولة الربط مع تطبيق Flutter".
3.  **Threshold (0.55):** قل "هذه هي عتبة القبول؛ أي مسافة أقل من 0.55 تعني أن الشخصين غالباً هما نفس الشخص".
4.  **Cosine Similarity:** هي الطريقة الرياضية التي يقيس بها الكمبيوتر "الزاوية" بين ملامح الوجهين ليحدد مدى التشابه.
5.  **Service Layer Pattern:** قل "فصلنا منطق التعرف على الوجوه في ملف `services.py` لجعل الكود قابلاً للاختبار (Testable) وسهل الصيانة".

---

## 4️⃣ لماذا هذا المشروع "نظيف" (High Quality)?
- **Settings Splitting:** الإعدادات مقسمة لبيئة التطوير وبيئة الإنتاج.
- **Environment Variables:** البيانات السرية مشفرة في ملف `.env`.
- **Zero Overhead:** تم حذف كل إضافات دجانجو غير المستخدمة (مثل نظام الصلاحيات) لزيادة السرعة.

بهذا الشرح والكود، أنت جاهز لمناقشة قوية جداً! أي جزء تقني تود التعمق فيه أكثر؟
