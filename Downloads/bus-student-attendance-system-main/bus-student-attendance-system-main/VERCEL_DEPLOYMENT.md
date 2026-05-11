# Vercel Deployment Guide - Bus Student Attendance System

## Prerequisites
- Vercel account (vercel.com)
- GitHub account (recommended)
- Project pushed to GitHub

## Local Setup for Testing

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

5. **Run development server:**
   ```bash
   python manage.py runserver
   ```

## Deploy to Vercel

### Method 1: Using Vercel CLI (Recommended)

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **Follow the prompts and select your project.**

### Method 2: Using GitHub Integration

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Select your GitHub repository
5. Configure environment variables in Vercel dashboard:
   - `DEBUG=False`
   - `SECRET_KEY=your-secret-key` (generate a new one)
   - `ALLOWED_HOSTS=your-domain.com,www.your-domain.com`
   - `DATABASE_URL=` (optional, for PostgreSQL)

6. Click "Deploy"

## Environment Variables to Set in Vercel

| Variable | Value | Notes |
|----------|-------|-------|
| `DEBUG` | `False` | Always False in production |
| `SECRET_KEY` | Generate new | Use Django's `get_random_secret_key()` |
| `ALLOWED_HOSTS` | Your domain | Comma-separated list |
| `DATABASE_URL` | PostgreSQL URL | Optional (uses SQLite by default) |

## Generate a New Secret Key

```python
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Important Notes

- **Database**: Currently uses SQLite. For production with multiple dynos, use PostgreSQL
- **Static Files**: Served by WhiteNoise (no additional S3 needed)
- **Media Files**: Consider using cloud storage (AWS S3, etc.) for production
- **Cold Starts**: First request may take 10-15 seconds

## Troubleshooting

### 404 on Static Files
- Ensure `python manage.py collectstatic --noinput` runs in build script
- Check `STATIC_ROOT` path in settings.py

### Database Errors
- For development: SQLite is fine
- For production: Use PostgreSQL with `DATABASE_URL`

### Secret Key Issues
- Generate a new secret key
- Update it in Vercel environment variables
- Redeploy

## Files Added for Vercel

- `vercel.json` - Vercel configuration
- `runtime.txt` - Python version
- `requirements.txt` - Updated with production packages
- `build.sh` - Build script
- `Procfile` - Gunicorn configuration
- `.gitignore` - Updated
- `.env.example` - Environment template

## Support

For issues, check:
- [Django Deployment Docs](https://docs.djangoproject.com/en/5.2/howto/deployment/)
- [Vercel Python Documentation](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
