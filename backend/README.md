# Django Backend - Calligraphy Learning Platform

Django REST Framework backend for the Calligraphy Learning Platform.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL (for production)
- pip

### Installation

1. **Clone the repository and navigate to backend:**
   ```bash
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

4. **Environment setup:**
   ```bash
   # Copy environment template
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Database setup:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server:**
   ```bash
   python manage.py runserver
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,api.mydomain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/calligraphy_db

# CORS Settings
CORS_ALLOWED_ORIGINS=https://mydomain.com,https://www.mydomain.com
CSRF_TRUSTED_ORIGINS=https://api.mydomain.com,https://mydomain.com
```

### Database Configuration

For **development** (SQLite):
```env
DATABASE_URL=sqlite:///db.sqlite3
```

For **production** (PostgreSQL):
```env
DATABASE_URL=postgresql://username:password@host:port/database_name
```

## 📁 Project Structure

```
backend/
├── core/                   # Django project settings
│   ├── settings.py        # Main settings file
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── users/                 # User management app
├── courses/               # Courses app
├── cart/                  # Shopping cart app
├── orders/                # Orders app
├── dashboard/             # Dashboard app
├── instructors/           # Instructors app
├── contact/               # Contact app
├── testimonials/          # Testimonials app
├── about/                 # About app
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration
└── .env                  # Environment variables
```

## 🌐 API Endpoints

### Authentication
- `POST /api/users/login/` - User login
- `POST /api/users/register/` - User registration
- `POST /api/users/logout/` - User logout
- `GET /api/users/user/` - Get current user

### Courses
- `GET /api/courses/` - List all courses
- `GET /api/courses/{id}/` - Get course details
- `POST /api/courses/` - Create new course (admin)
- `PUT /api/courses/{id}/` - Update course (admin)
- `DELETE /api/courses/{id}/` - Delete course (admin)

### Cart
- `GET /api/cart/` - Get user cart
- `POST /api/cart/` - Add item to cart
- `PUT /api/cart/items/{id}/` - Update cart item
- `DELETE /api/cart/items/{id}/` - Remove item from cart

### Orders
- `GET /api/orders/` - List user orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Get order details

## 🔒 Security

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up `CSRF_TRUSTED_ORIGINS`
- [ ] Configure CORS properly
- [ ] Use HTTPS in production
- [ ] Set up proper database
- [ ] Configure static files
- [ ] Set up logging

### JWT Configuration

The project uses JWT tokens for authentication:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

## 🚀 Deployment

### Cloudflare Tunnel

1. **Install cloudflared:**
   ```bash
   # Download from https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
   ```

2. **Create tunnel:**
   ```bash
   cloudflared tunnel create calligraphy-backend
   ```

3. **Configure tunnel:**
   ```bash
   cloudflared tunnel route dns calligraphy-backend api.mydomain.com
   ```

4. **Create config file (`config.yml`):**
   ```yaml
   tunnel: your-tunnel-id
   credentials-file: /path/to/credentials.json
   
   ingress:
     - hostname: api.mydomain.com
       service: http://localhost:8000
     - service: http_status:404
   ```

5. **Run tunnel:**
   ```bash
   cloudflared tunnel run calligraphy-backend
   ```

### Production Commands

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start with gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

## 📊 Management Commands

### Create Sample Data
```bash
python manage.py create_sample_about
```

### Database Operations
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test courses
```

## 📝 Logging

Configure logging in `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🔧 Troubleshooting

### Common Issues

1. **Database connection errors:**
   - Check `DATABASE_URL` in `.env`
   - Ensure PostgreSQL is running
   - Verify database credentials

2. **CORS errors:**
   - Check `CORS_ALLOWED_ORIGINS` in `.env`
   - Ensure frontend URL is included

3. **Static files not loading:**
   - Run `python manage.py collectstatic`
   - Check `STATIC_ROOT` configuration

4. **JWT token issues:**
   - Check token expiration settings
   - Verify `SECRET_KEY` is set

## 📞 Support

For issues and questions, please check the main project README or create an issue in the repository. 