## Setup Instructions

### 🚀 Easy Setup (Windows)
Just double-click the `setup_and_run.bat` file. It will:
1. Create a virtual environment.
2. Install all required libraries (including AI models).
3. Setup the database.
4. Start the server.

### 🐧 Easy Setup (Linux/Mac)
Run `sh setup.sh` in your terminal.

## Features
- RESTful API for managing missing persons reports
- Image upload support
- MongoDB Atlas integration
- CORS enabled for Flutter frontend
- Image search endpoint (placeholder for AI integration)

## Tech Stack
- Django 3.1.12
- Django REST Framework 3.12.4
- Djongo (MongoDB connector)
- MongoDB Atlas

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment
**Windows:**
```bash
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database
The MongoDB connection is already configured in `findme_backend/settings.py`. Make sure the connection string is correct.

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

## API Endpoints

### Missing Persons
- **GET** `/api/missing-persons/` - List all missing persons
- **POST** `/api/missing-persons/` - Create new missing person report
- **GET** `/api/missing-persons/{id}/` - Get specific missing person
- **PUT** `/api/missing-persons/{id}/` - Update missing person
- **DELETE** `/api/missing-persons/{id}/` - Delete missing person
- **POST** `/api/missing-persons/search-by-image/` - Search by image (placeholder)

### Admin Panel
Access the Django admin panel at: `http://127.0.0.1:8000/admin/`

## Project Structure
```
Backend/
├── api/                    # Main API app
│   ├── models.py          # MissingPerson model
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── urls.py            # API routes
│   └── admin.py           # Admin configuration
├── findme_backend/        # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── media/                 # Uploaded images
├── venv/                  # Virtual environment
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Flutter Integration
The Flutter app should point to:
- **Windows/iOS Simulator:** `http://127.0.0.1:8000/api`
- **Android Emulator:** `http://10.0.2.2:8000/api`

## Notes
- CORS is enabled for all origins in development
- Media files are served in DEBUG mode
- MongoDB Atlas is used for data storage
- Image search endpoint is a placeholder for future AI integration
