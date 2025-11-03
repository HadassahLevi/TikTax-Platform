# 🚀 Tik-Tax Backend - Quick Start Guide

## Step-by-Step Setup (5 minutes)

### 1️⃣ Install Python Dependencies
```powershell
cd C:\TikTax\backend

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### 2️⃣ Generate Secret Key
```powershell
# Run this to generate a secure secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3️⃣ Configure Environment
```powershell
# Copy the template
copy .env.example .env

# Edit .env and replace:
# - SECRET_KEY with the key from step 2
# - DATABASE_URL with your PostgreSQL connection string
#   Example: postgresql://username:password@localhost:5432/tiktax
```

### 4️⃣ Set Up Database
```powershell
# Option A: Create database using psql
psql -U postgres -c "CREATE DATABASE tiktax;"

# Option B: Create database using pgAdmin
# (Use the GUI to create a database named 'tiktax')

# Run migrations
alembic upgrade head

# Seed default categories
python -m app.db.init_db
```

### 5️⃣ Run the Server
```powershell
# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the built-in runner
python -m app.main
```

### 6️⃣ Test the API
```powershell
# Open your browser:
http://localhost:8000/health          # Should return {"status": "healthy"}
http://localhost:8000/api/v1/docs     # Interactive API documentation
```

## 📋 Minimal .env Configuration

For development, you can start with this minimal `.env`:

```env
# Security (REQUIRED)
SECRET_KEY=your-generated-secret-key-from-step-2
ALGORITHM=HS256

# Database (REQUIRED)
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/tiktax

# Frontend (REQUIRED)
FRONTEND_URL=http://localhost:5173

# External Services (OPTIONAL - can add later)
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
# AWS_S3_BUCKET=
# GOOGLE_CLOUD_VISION_CREDENTIALS=
# TWILIO_ACCOUNT_SID=
# TWILIO_AUTH_TOKEN=
# TWILIO_PHONE_NUMBER=
# SENDGRID_API_KEY=
# SENDGRID_FROM_EMAIL=
```

## ✅ Verify Installation

### Check Dependencies
```powershell
pip list | Select-String "fastapi|uvicorn|sqlalchemy|pydantic"
```

Should show:
- fastapi 0.104.1
- uvicorn 0.24.0
- sqlalchemy 2.0.23
- pydantic 2.5.1

### Check Database Connection
```powershell
python -c "from app.db.session import SessionLocal; db = SessionLocal(); db.execute('SELECT 1'); print('✅ Database connected'); db.close()"
```

### Check API Health
```powershell
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "database": "healthy",
  "version": "1.0.0"
}
```

## 🔥 Common Issues & Solutions

### Issue: `ModuleNotFoundError: No module named 'fastapi'`
**Solution:** Activate virtual environment
```powershell
.\venv\Scripts\activate
```

### Issue: `could not connect to server: Connection refused`
**Solution:** Start PostgreSQL service
```powershell
# Windows:
net start postgresql-x64-13  # Adjust version number

# Or use pgAdmin to start the server
```

### Issue: `SECRET_KEY not found`
**Solution:** Copy and edit .env file
```powershell
copy .env.example .env
# Then edit .env with your values
```

### Issue: Import errors in VS Code
**Solution:** These will disappear after installing dependencies. If they persist:
1. Select Python interpreter: Ctrl+Shift+P → "Python: Select Interpreter"
2. Choose the venv interpreter: `.\venv\Scripts\python.exe`

## 🎯 Next Steps

### 1. Implement Authentication Endpoints
Edit `app/api/v1/endpoints/auth.py` and implement:
- `signup()` - User registration
- `login()` - User authentication
- `refresh_token()` - Token refresh

### 2. Implement Receipt Upload
Edit `app/api/v1/endpoints/receipts.py` and implement:
- `upload_receipt()` - Handle file upload and OCR

### 3. Integrate External Services
- Google Cloud Vision (OCR)
- AWS S3 (File storage)
- Twilio (SMS)
- SendGrid (Email)

### 4. Run Tests
```powershell
# Install test dependencies (already in requirements.txt)
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## 📚 Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLAlchemy ORM**: https://docs.sqlalchemy.org/en/20/orm/
- **Pydantic**: https://docs.pydantic.dev
- **Alembic**: https://alembic.sqlalchemy.org

## 🎉 You're Ready!

Your backend is now set up and running. Check out:
- `SETUP_COMPLETE.md` for full feature list
- `README.md` for comprehensive documentation
- Code comments for implementation guidance

**Happy coding! 🚀**
