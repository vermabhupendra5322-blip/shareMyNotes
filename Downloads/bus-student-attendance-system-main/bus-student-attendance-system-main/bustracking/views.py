from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from datetime import timedelta
import qrcode

from .models import Student, BusEntry, Bus
from .forms import StudentRegistrationForm, BusForm, BoardingForm, ExitForm


def home(request):
    """Landing page with login/register links"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('student_dashboard')

    total_buses = Bus.objects.filter(is_active=True).count()
    total_students = Student.objects.filter(is_active=True).count()
    return render(request, 'home.html', {
        'total_buses': total_buses,
        'total_students': total_students,
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')

    form = StudentRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        place = form.cleaned_data['place']
        bus = form.cleaned_data['bus']
        password = form.cleaned_data['password']

        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
        else:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
            Student.objects.create(
                user=user,
                name=name,
                email=email,
                place=place,
                bus=bus,
            )
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('student_dashboard')

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('student_dashboard')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        if user.is_staff:
            return redirect('admin_dashboard')
        return redirect('student_dashboard')

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def student_is_authenticated(user):
    return user.is_authenticated and not user.is_staff


def admin_is_authenticated(user):
    return user.is_authenticated and user.is_staff


@login_required(login_url='login')
@user_passes_test(student_is_authenticated, login_url='login')
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    today = timezone.now().date()
    today_entries = student.bus_entries.filter(date=today).order_by('-entry_time')
    active_entry = today_entries.filter(exit_time__isnull=True).last()
    boarding_form = BoardingForm()
    exit_form = ExitForm()

    weekly_start = today - timedelta(days=6)
    weekly_records = student.bus_entries.filter(date__gte=weekly_start).values('date').annotate(count=Count('id')).order_by('date')
    weekly_data = []
    for day_index in range(7):
        day = weekly_start + timedelta(days=day_index)
        count = next((item['count'] for item in weekly_records if item['date'] == day), 0)
        weekly_data.append({
            'day': day.strftime('%a'),
            'count': count,
            'height': min(count * 20 + 30, 170),
        })

    total_week_trips = sum(item['count'] for item in weekly_data)
    current_status = 'Boarded' if active_entry else 'Not boarded'

    return render(request, 'student_dashboard.html', {
        'student': student,
        'today_entries': today_entries,
        'active_entry': active_entry,
        'boarding_form': boarding_form,
        'exit_form': exit_form,
        'weekly_data': weekly_data,
        'total_week_trips': total_week_trips,
        'current_status': current_status,
    })


@login_required(login_url='login')
@user_passes_test(student_is_authenticated, login_url='login')
@require_http_methods(['POST'])
def mark_boarding(request):
    student = get_object_or_404(Student, user=request.user)
    if not student.bus:
        messages.error(request, 'Your bus is not assigned. Please contact the administrator.')
        return redirect('student_dashboard')

    form = BoardingForm(request.POST)
    if form.is_valid():
        today = timezone.now().date()
        active_entry = BusEntry.objects.filter(
            student=student,
            exit_time__isnull=True,
            date=today
        ).first()
        if active_entry:
            messages.warning(request, 'You already have an active boarding record today.')
            return redirect('student_dashboard')

        BusEntry.objects.create(
            bus=student.bus,
            student=student,
            boarding_place=form.cleaned_data['boarding_place'],
            entry_time=timezone.now(),
            source='MANUAL',
        )
        messages.success(request, 'Boarding time recorded successfully.')
    else:
        messages.error(request, 'Please provide the boarding place.')

    return redirect('student_dashboard')


@login_required(login_url='login')
@user_passes_test(student_is_authenticated, login_url='login')
@require_http_methods(['POST'])
def mark_exit(request):
    student = get_object_or_404(Student, user=request.user)
    active_entry = BusEntry.objects.filter(
        student=student,
        exit_time__isnull=True,
        date=timezone.now().date()
    ).last()

    if not active_entry:
        messages.warning(request, 'No active boarding record found.')
        return redirect('student_dashboard')

    form = ExitForm(request.POST)
    if form.is_valid():
        active_entry.exit_place = form.cleaned_data['exit_place']
        active_entry.exit_time = timezone.now()
        active_entry.save()
        messages.success(request, 'Exit time recorded successfully.')
    else:
        messages.error(request, 'Please provide the exit place.')

    return redirect('student_dashboard')


@login_required(login_url='login')
@user_passes_test(student_is_authenticated, login_url='login')
def scan_bus(request, bus_id):
    student = get_object_or_404(Student, user=request.user)
    bus = get_object_or_404(Bus, id=bus_id, is_active=True)

    if student.bus_id != bus.id:
        messages.error(request, 'This bus is not assigned to your registration.')
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = BoardingForm(request.POST)
        if form.is_valid():
            today = timezone.now().date()
            active_entry = BusEntry.objects.filter(
                student=student,
                exit_time__isnull=True,
                date=today
            ).first()
            if active_entry:
                messages.warning(request, 'You already have an active boarding record today.')
                return redirect('student_dashboard')

            BusEntry.objects.create(
                bus=bus,
                student=student,
                boarding_place=form.cleaned_data['boarding_place'],
                entry_time=timezone.now(),
                source='QR',
            )
            messages.success(request, 'QR scan successful. Boarding time recorded.')
            return redirect('student_dashboard')
    else:
        form = BoardingForm()

    return render(request, 'scan.html', {
        'bus': bus,
        'student': student,
        'form': form,
    })


@login_required(login_url='login')
@user_passes_test(admin_is_authenticated, login_url='login')
def admin_dashboard(request):
    buses = Bus.objects.filter(is_active=True)
    form = BusForm(request.POST or None)
    today = timezone.now().date()
    entries = BusEntry.objects.select_related('student', 'bus').filter(date=today).order_by('-entry_time')
    total_students = Student.objects.filter(is_active=True).count()
    total_buses = buses.count()
    unique_present = entries.values('student').distinct().count()
    onboard_count = entries.filter(exit_time__isnull=True).count()
    absent_students = max(total_students - unique_present, 0)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'New bus added successfully.')
        return redirect('admin_dashboard')

    return render(request, 'admin_dashboard.html', {
        'buses': buses,
        'entries': entries,
        'form': form,
        'today': today,
        'total_students': total_students,
        'total_buses': total_buses,
        'onboard_count': onboard_count,
        'absent_students': absent_students,
        'scan_count': entries.count(),
        'unique_present': unique_present,
    })


@login_required(login_url='login')
@user_passes_test(admin_is_authenticated, login_url='login')
def generate_qr_code(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    scan_url = request.build_absolute_uri(reverse('scan_bus', args=[bus.id]))
    qr_data = f"{scan_url}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    response = HttpResponse(content_type='image/png')
    img.save(response, 'PNG')
    return response


@login_required(login_url='login')
@user_passes_test(student_is_authenticated, login_url='login')
def student_report(request):
    student = get_object_or_404(Student, user=request.user)
    days = request.GET.get('days', 30)
    try:
        days = int(days)
    except ValueError:
        days = 30

    start_date = timezone.now().date() - timedelta(days=days)
    records = BusEntry.objects.filter(student=student, date__gte=start_date).order_by('-date', '-entry_time')
    total_trips = records.count()
    total_time_in_bus = sum([
        (r.exit_time - r.entry_time).total_seconds()
        for r in records if r.exit_time
    ]) / 3600

    return render(request, 'student_report.html', {
        'student': student,
        'records': records,
        'total_trips': total_trips,
        'total_time_in_bus': round(total_time_in_bus, 2),
        'days': days,
    })


@login_required(login_url='login')
@user_passes_test(admin_is_authenticated, login_url='login')
def bus_report(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    today = timezone.now().date()
    records = BusEntry.objects.filter(bus=bus, date=today).order_by('entry_time')
    unique_students = records.values('student').distinct().count()
    current_passengers = records.filter(exit_time__isnull=True).count()

    return render(request, 'bus_report.html', {
        'bus': bus,
        'records': records,
        'unique_students': unique_students,
        'current_passengers': current_passengers,
    })

def bus_report(request, bus_id):
    """Display bus route report for the day"""
    bus = get_object_or_404(Bus, id=bus_id)
    
    today = timezone.now().date()
    records = BusEntry.objects.filter(
        bus=bus,
        date=today
    ).order_by('entry_time')
    
    # Calculate unique students
    unique_students = records.values('student').distinct().count()
    current_passengers = BusEntry.objects.filter(
        bus=bus,
        exit_time__isnull=True,
        date=today
    ).count()
    
    context = {
        'bus': bus,
        'records': records,
        'unique_students': unique_students,
        'current_passengers': current_passengers,
    }
    
    return render(request, 'bus_report.html', context)
