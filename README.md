# 🔍 FindMe Backend (Minimalist Engine)

A high-performance, lightweight Django-based backend for missing person identification using **Facial Recognition**. This project has been stripped of all unnecessary Django overhead (no admin, no auth, no sessions) to provide a blazing-fast API focused solely on person matching.

## 🚀 Key Features

- **⚡ Lightweight Core:** Removed unused Django apps (Auth, Admin, Sessions) for a zero-bloat database.
- **🖼️ Face Matching:** Integrated **DeepFace** (Facenet512) for high-accuracy facial identification.
- **📍 Location Ready:** Schema support for geo-coordinates (Lat/Long) and physical descriptions.
- **🛠️ Service-Oriented:** Clean architecture with a dedicated `FaceRecognitionService`.

## 📁 Project structure

```text
Backend/
├── api/                # Core Logic
│   ├── migrations/     # Database snapshots
│   ├── models.py       # MissingPerson schema
│   ├── views.py        # Clean API endpoints
│   ├── services.py     # DeepFace processing logic
│   └── serializers.py  # Data formatting
├── findme_project/     # Configuration
│   └── settings/       # Environment-specific settings
│       ├── base.py     # Base config
│       ├── local.py    # Dev config
│       └── production.py # Server config
├── requirements/       # Dependency management
├── .env.example        # Environment template
└── manage.py           # CLI Tool
```

## 🛠️ Installation & Setup

1. **Environmental Variables:**
   ```bash
   cp .env.example .env
   # Update your MONGO_URI in .env
   ```

2. **Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Initialization:**
   ```bash
   python manage.py makemigrations api
   python manage.py migrate
   ```

4. **Launch:**
   ```bash
   python manage.py runserver
   ```

## 🔗 Main API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/missing-persons/` | `GET/POST` | List or register a missing person |
| `/api/missing-persons/{id}/` | `GET/PUT` | View or update specific record |
| `/api/missing-persons/search-by-image/` | `POST` | **Search using facial recognition** |

---
*Maintained by Antigravity AI Engine.*
