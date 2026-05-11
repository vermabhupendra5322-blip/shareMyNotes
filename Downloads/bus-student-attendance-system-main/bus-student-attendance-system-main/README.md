# Bus Student Attendance System

A comprehensive Django-based web application for tracking student bus entry and exit with QR code scanning capability. The system helps bus incharges and administrators monitor student transportation efficiently.

## Features

### Core Features
- ✅ **QR Code Scanning**: Each bus has a unique QR code for quick student identification
- ✅ **Student Entry/Exit Recording**: Automatic timestamp recording for bus boarding and alighting
- ✅ **Real-time Dashboard**: Comprehensive dashboard showing daily attendance data
- ✅ **Bus Management**: Track bus routes, driver information, and capacity
- ✅ **Student Records**: Maintain detailed student information and travel history
- ✅ **Report Generation**: Individual student reports and bus-wise statistics
- ✅ **Admin Interface**: Built-in Django admin panel for data management

### Business Logic
- Prevents duplicate entry records for the same student on the same bus
- Calculates time spent in bus for each trip
- Filters by bus and date for detailed analysis
- Tracks current passengers on each bus
- Provides comprehensive travel history for each student

## Project Structure

```
bustracking/
├── manage.py                 # Django management script
├── db.sqlite3               # Database file
├── populate_data.py         # Script to populate sample data
├── static/                  # Static files (CSS, JS, Images)
├── bustracking/
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── asgi.py              # ASGI configuration
│   ├── wsgi.py              # WSGI configuration
│   ├── models.py            # Database models (Bus, Student, BusEntry)
│   ├── views.py             # View logic
│   ├── admin.py             # Admin interface configuration
│   ├── migrations/          # Database migrations
│   └── templates/           # HTML templates
│       ├── base.html        # Base template with styling
│       ├── home.html        # Home page with bus selection
│       ├── dashboard.html   # Attendance dashboard
│       ├── success.html     # Success/Status messages
│       ├── student_report.html   # Individual student report
│       └── bus_report.html   # Bus-wise report
└── README.md
```

## Database Models

### Bus Model
Stores information about each bus service:
- UUID (unique identifier)
- Name of the bus
- Route information
- Capacity
- Driver details (name, phone)
- Active status
- Creation and update timestamps

### Student Model
Maintains student information:
- Name
- Roll number (unique)
- Email address (unique)
- Phone number
- Assigned bus
- Active status
- Creation and update timestamps

### BusEntry Model
Records each entry/exit event:
- Reference to Bus
- Reference to Student
- Entry time (automatically recorded)
- Exit time (recorded when student exits)
- Date of travel
- Creation timestamp

## Installation & Setup

### Prerequisites
- Python 3.8+
- Django 5.2.1
- qrcode library
- Pillow (for image processing)

### Step 1: Install Dependencies
```bash
pip install django qrcode pillow
```

### Step 2: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
When prompted, enter:
- Username: admin
- Email: admin@bustracking.com
- Password: (enter your secure password)

### Step 4: Populate Sample Data (Optional)
To add sample buses and students for testing:
```bash
python populate_data.py
```

### Step 5: Run Development Server
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## Usage

### Home Page (`/`)
- Select a bus and student
- Click "Entry" to record student boarding
- Click "Exit" to record student alighting
- QR codes are displayed for each bus

### Dashboard (`/dashboard/`)
- View all attendance records
- Filter by bus and date
- See bus-wise statistics
- Track currently active passengers

### Student Report (`/student-report/<student_id>/`)
Shows:
- Individual student travel history
- Total trips taken
- Total time spent in bus
- Filter by number of days

### Bus Report (`/bus-report/<bus_id>/`)
Shows:
- Bus route details
- Today's passenger list
- Time duration for each trip
- Current passenger count

### Admin Panel (`/admin/`)
Username: admin
Password: (as set during setup)

Features:
- Manage buses (add, edit, delete)
- Manage students
- View and manage attendance records
- Search and filter functionality

## QR Code System

Each bus has a unique QR code that contains:
- Bus UUID
- Bus ID
- Bus Name

### Scanning Process
1. Student opens the application
2. Selects their bus from the home page
3. Can either:
   - Manually click "Entry" or "Exit" buttons
   - Scan the bus's QR code using a mobile app (for future implementation)

## Key API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Home page with bus selection |
| `/entry/<bus_id>/<student_id>/` | GET/POST | Record student entry |
| `/exit/<bus_id>/<student_id>/` | GET/POST | Record student exit |
| `/dashboard/` | GET | View attendance dashboard |
| `/student-report/<student_id>/` | GET | View student's travel history |
| `/bus-report/<bus_id>/` | GET | View bus statistics |
| `/qr-code/<bus_id>/` | GET | Generate QR code image |
| `/admin/` | GET | Django admin panel |

## File Descriptions

### Models (models.py)
- **Bus**: Bus information with UUID, route, driver details
- **Student**: Student information with bus assignment
- **BusEntry**: Travel records with entry/exit timestamps

### Views (views.py)
- `home()`: Main interface with bus selection
- `entry()`: Record student entry with duplicate check
- `exit_bus()`: Record student exit with duration calculation
- `dashboard()`: Comprehensive attendance dashboard
- `student_report()`: Individual student travel history
- `bus_report()`: Bus-wise statistics
- `generate_qr_code()`: Generate QR code for bus

### Admin (admin.py)
- Customized admin interfaces for all models
- Fieldsets for organized form display
- Search and filter capabilities
- Read-only fields for audit trail

## Security Features

- Admin panel requires authentication
- CSRF protection enabled
- Session management
- Input validation
- Database relationships with foreign keys

## Future Enhancements

1. **Mobile Application**
   - Native mobile apps for QR code scanning
   - Real-time status updates
   - Push notifications for late buses

2. **SMS/Email Notifications**
   - Send notifications to parents/guardians
   - Daily attendance reports
   - Alert for missed pickups

3. **GPS Integration**
   - Real-time bus location tracking
   - Route optimization

4. **Advanced Analytics**
   - Attendance patterns
   - Peak hours analysis
   - Predictive analytics

5. **Payment Integration**
   - Bus fare management
   - Digital payments

6. **API for Third-party Integration**
   - RESTful API
   - Mobile app backend

## Troubleshooting

### Issue: "static directory does not exist"
**Solution**: Create the static folder
```bash
mkdir static
```

### Issue: Database locked
**Solution**: Delete db.sqlite3 and run migrations again
```bash
rm db.sqlite3
python manage.py migrate
```

### Issue: Port 8000 already in use
**Solution**: Use a different port
```bash
python manage.py runserver 8001
```

### Issue: Import error for qrcode
**Solution**: Install qrcode package
```bash
pip install qrcode pillow
```

## Configuration

### Settings to Customize (in settings.py)

1. **Debug Mode**
   ```python
   DEBUG = False  # For production
   ```

2. **Allowed Hosts**
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

3. **Database** (for production, use PostgreSQL or MySQL)
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'bustracking',
       }
   }
   ```

4. **Time Zone**
   ```python
   TIME_ZONE = 'Asia/Kolkata'  # Already set for India
   ```

## Tech Stack

- **Backend**: Python 3.13
- **Framework**: Django 5.2.1
- **Database**: SQLite (development), PostgreSQL/MySQL (production)
- **Frontend**: HTML5, CSS3
- **QR Code**: qrcode library
- **Image Processing**: Pillow

## License

This project is developed for educational purposes.

## Support

For issues or questions, please refer to:
- Django Documentation: https://docs.djangoproject.com/
- QRCode Documentation: https://github.com/lincolnloop/python-qrcode

## Author

Bus Student Attendance System
Educational Project

---

**Last Updated**: May 2026
**Version**: 1.0
