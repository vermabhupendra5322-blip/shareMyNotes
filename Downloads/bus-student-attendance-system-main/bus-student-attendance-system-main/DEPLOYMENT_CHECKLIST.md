# Vercel Deployment Checklist ✅

## Before Deployment

- [ ] Read `VERCEL_DEPLOYMENT.md` for complete guide
- [ ] Generate a new SECRET_KEY:
  ```bash
  python manage.py shell
  from django.core.management.utils import get_random_secret_key
  print(get_random_secret_key())
  ```
- [ ] Copy new SECRET_KEY somewhere safe
- [ ] Commit all changes: `git add -A && git commit -m "Prepare for Vercel deployment"`
- [ ] Push to GitHub: `git push origin main`

## Vercel Setup

- [ ] Go to [vercel.com](https://vercel.com)
- [ ] Sign in with GitHub account
- [ ] Click "New Project"
- [ ] Select your repository
- [ ] Add Environment Variables:
  - [ ] `DEBUG` = `False`
  - [ ] `SECRET_KEY` = your-generated-key
  - [ ] `ALLOWED_HOSTS` = your-domain.com,www.your-domain.com
  - [ ] `DATABASE_URL` = (leave empty for SQLite, or add PostgreSQL URL)
- [ ] Click "Deploy"

## After Deployment

- [ ] Test the deployed URL in browser
- [ ] Check that static files load (CSS/JS)
- [ ] Test login/registration
- [ ] Check Vercel logs for any errors: `Deployments → Select Latest → Function Logs`

## For Database Issues

If you see database errors:

1. **Option 1: Use PostgreSQL** (Recommended for production)
   - Get PostgreSQL URL from your provider (Heroku PostgreSQL, Vercel Postgres, etc.)
   - Set `DATABASE_URL` environment variable
   - Migrations will run automatically via `build.sh`

2. **Option 2: Keep SQLite** (Limited, but works for small projects)
   - Current setup uses SQLite locally
   - Initial data won't persist across deployments
   - For persistent data, use PostgreSQL

## Quick Test Locally

Before deploying, test build process:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

Visit `http://localhost:8000` to verify everything works.

## Generated Files Summary

| File | Purpose |
|------|---------|
| `vercel.json` | Vercel configuration |
| `runtime.txt` | Python 3.11.9 version |
| `requirements.txt` | Updated with production packages |
| `build.sh` | Build script (migrations, static files) |
| `Procfile` | Gunicorn configuration |
| `.env.example` | Environment variables template |
| `.gitignore` | Git ignore rules |
| `VERCEL_DEPLOYMENT.md` | Complete deployment guide |
| `DEPLOYMENT_CHECKLIST.md` | This file |

## Need Help?

- Check Vercel logs: Deployments → Latest → Function Logs
- Django Debug Toolbar won't work on Vercel (DEBUG=False)
- For local development: Create `.env` with DEBUG=True
- Refer to `VERCEL_DEPLOYMENT.md` for troubleshooting
