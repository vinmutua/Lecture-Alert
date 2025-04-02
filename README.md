# Lecture Alert System

A Django-based system for managing lecture schedules and notifications.

## Features

- Lecturer and Admin authentication
- Course and Department management
- Lecture schedule management
- SMS notifications using Infobip
- Celery for background tasks

## Prerequisites

- Python 3.8+
- MySQL
- Redis
- Git

## Installation

1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd lecture_alert
```

2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations
```bash
python manage.py migrate
```

6. Start development server
```bash
python manage.py runserver
```

## Environment Variables

Copy `.env.example` to `.env` and update the values:

- `DEBUG`: Set to False in production
- `SECRET_KEY`: Django secret key
- `DB_*`: Database configuration
- `INFOBIP_*`: Infobip SMS configuration
- `CELERY_*`: Celery configuration

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

