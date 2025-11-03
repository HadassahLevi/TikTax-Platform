# Tik-Tax Backend API

Production-ready FastAPI backend for the Tik-Tax receipt management platform.

## 🚀 Features

- **Authentication**: JWT-based auth with access/refresh tokens
- **Receipt Management**: Upload, OCR processing, CRUD operations
- **OCR Integration**: Google Cloud Vision for Hebrew receipt text extraction
- **File Storage**: AWS S3 for secure receipt image storage
- **Export**: Excel and PDF generation for accountants
- **SMS Verification**: Twilio integration for phone verification
- **Email**: SendGrid for transactional emails
- **Subscriptions**: Stripe integration for payment management
- **Israeli Support**: Validators for Israeli ID, phone, business ID

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/v1/endpoints/    # API endpoints
│   ├── core/                # Configuration, security, dependencies
│   ├── db/                  # Database setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── utils/               # Utilities
│   ├── middleware/          # Custom middleware
│   └── main.py              # FastAPI app initialization
├── alembic/                 # Database migrations
├── tests/                   # Test suite
├── requirements.txt         # Dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

## 🛠️ Setup

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Redis (optional, for rate limiting)

### Installation

1. **Clone repository:**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Set up database:**
   ```bash
   # Create database
   createdb tiktax

   # Run migrations
   alembic upgrade head

   # Seed initial data
   python -m app.db.init_db
   ```

## 🔐 Environment Variables

See `.env.example` for all required environment variables:

- **SECRET_KEY**: JWT secret (generate with `openssl rand -hex 32`)
- **DATABASE_URL**: PostgreSQL connection string
- **AWS credentials**: S3 bucket access
- **GOOGLE_CLOUD_VISION_CREDENTIALS**: Path to GCP credentials JSON
- **TWILIO credentials**: SMS service
- **SENDGRID_API_KEY**: Email service

## 🏃 Running the Application

### Development

```bash
# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the built-in runner:
```bash
python -m app.main
```

### Production

```bash
# Using Gunicorn with Uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📚 API Documentation

Once running, access interactive API docs:

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/api/test_auth.py
```

## 🗄️ Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## 📋 API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/send-sms` - Send SMS verification
- `POST /api/v1/auth/verify-sms` - Verify SMS code

### Receipts
- `POST /api/v1/receipts/upload` - Upload receipt image
- `GET /api/v1/receipts` - Get user receipts (with filters)
- `GET /api/v1/receipts/{id}` - Get single receipt
- `PUT /api/v1/receipts/{id}` - Update receipt
- `DELETE /api/v1/receipts/{id}` - Delete receipt

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update profile
- `DELETE /api/v1/users/me` - Delete account

### Categories
- `GET /api/v1/categories` - Get all categories

### Export
- `GET /api/v1/export/excel` - Export to Excel
- `GET /api/v1/export/pdf/{id}` - Export receipt to PDF

### Subscriptions
- `GET /api/v1/subscriptions/status` - Get subscription status
- `POST /api/v1/subscriptions/create-checkout-session` - Create Stripe session
- `POST /api/v1/subscriptions/webhook` - Stripe webhook

## 🛡️ Security

- JWT tokens with access/refresh pattern
- Password hashing with bcrypt
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy ORM
- Rate limiting middleware
- CORS configuration
- Environment-based secrets

## 🌍 Israeli Support

The API includes specialized support for Israeli businesses:

- **ID Validation**: Israeli ID number validation with Luhn algorithm
- **Phone Validation**: Israeli phone number formats (mobile + landline)
- **Business ID Validation**: Israeli business ID (ח.ב / ע.מ)
- **Currency**: ILS (₪) formatting
- **Date Format**: DD/MM/YYYY
- **VAT Calculation**: 17% Israeli VAT
- **Hebrew OCR**: Optimized for Hebrew text extraction

## 📦 Deployment

### Docker (Coming Soon)

```bash
docker build -t tiktax-api .
docker run -p 8000:8000 tiktax-api
```

### Cloud Platforms

Compatible with:
- AWS (EC2, ECS, Lambda)
- Google Cloud (Cloud Run, App Engine)
- Heroku
- DigitalOcean

## 🔧 Development

### Code Style

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

### Adding New Endpoints

1. Create endpoint in `app/api/v1/endpoints/`
2. Add Pydantic schemas in `app/schemas/`
3. Implement business logic in `app/services/`
4. Add tests in `tests/api/`
5. Register router in `app/api/v1/router.py`

## 📝 License

Proprietary - Tik-Tax Platform

## 👥 Contributors

- Development Team: [Your Team]

## 📞 Support

For support, email: support@tiktax.co.il
