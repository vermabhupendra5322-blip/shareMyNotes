#!/usr/bin/env python
"""Script to populate sample data into the database"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bustracking.settings')
django.setup()

from bustracking.models import Bus, Student

# Clear existing data
Bus.objects.all().delete()
Student.objects.all().delete()

# Create sample buses
buses = [
    Bus.objects.create(
        name='Bus A-01',
        route='Main Campus to Girls Hostel',
        capacity=45,
        driver_name='Harish Kumar',
        driver_phone='9876543210'
    ),
    Bus.objects.create(
        name='Bus A-02',
        route='Main Campus to Boys Hostel',
        capacity=50,
        driver_name='Rajesh Singh',
        driver_phone='9876543211'
    ),
    Bus.objects.create(
        name='Bus B-01',
        route='City Center to Main Campus',
        capacity=40,
        driver_name='Amit Patel',
        driver_phone='9876543212'
    ),
    Bus.objects.create(
        name='Bus B-02',
        route='Railway Station to Main Campus',
        capacity=48,
        driver_name='Vikram Sharma',
        driver_phone='9876543213'
    ),
]

# Create sample students
students_data = [
    ('Rahul Sharma', 'CSE-2024-001', 'rahul.sharma@example.com', '9876543220'),
    ('Priya Singh', 'CSE-2024-002', 'priya.singh@example.com', '9876543221'),
    ('Aditya Kumar', 'CSE-2024-003', 'aditya.kumar@example.com', '9876543222'),
    ('Neha Gupta', 'CSE-2024-004', 'neha.gupta@example.com', '9876543223'),
    ('Vikas Reddy', 'CSE-2024-005', 'vikas.reddy@example.com', '9876543224'),
    ('Anjali Verma', 'CSE-2024-006', 'anjali.verma@example.com', '9876543225'),
    ('Arjun Singh', 'ECE-2024-001', 'arjun.singh@example.com', '9876543226'),
    ('Divya Nair', 'ECE-2024-002', 'divya.nair@example.com', '9876543227'),
    ('Sanjay Rao', 'ECE-2024-003', 'sanjay.rao@example.com', '9876543228'),
    ('Kavya Iyer', 'ECE-2024-004', 'kavya.iyer@example.com', '9876543229'),
    ('Ravi Kumar', 'ME-2024-001', 'ravi.kumar@example.com', '9876543230'),
    ('Pooja Desai', 'ME-2024-002', 'pooja.desai@example.com', '9876543231'),
    ('Nikhil Joshi', 'ME-2024-003', 'nikhil.joshi@example.com', '9876543232'),
    ('Shreya Bansal', 'ME-2024-004', 'shreya.bansal@example.com', '9876543233'),
    ('Varun Malhotra', 'IT-2024-001', 'varun.malhotra@example.com', '9876543234'),
]

for i, (name, roll_number, email, phone) in enumerate(students_data):
    bus = buses[i % len(buses)]
    Student.objects.create(
        name=name,
        roll_number=roll_number,
        email=email,
        phone_number=phone,
        bus=bus
    )

print(f"✓ Created {len(buses)} buses")
print(f"✓ Created {len(students_data)} students")
print("\nSample Data Created Successfully!")
print("\nBuses:")
for bus in Bus.objects.all():
    print(f"  - {bus.name} ({bus.route}) - Driver: {bus.driver_name}")

print("\nStudents:")
for student in Student.objects.all():
    print(f"  - {student.name} ({student.roll_number}) - Bus: {student.bus.name if student.bus else 'Not Assigned'}")
