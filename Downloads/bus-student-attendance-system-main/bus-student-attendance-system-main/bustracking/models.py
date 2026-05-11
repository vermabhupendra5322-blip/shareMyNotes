from django.db import models
from django.contrib.auth.models import User
import uuid


class Bus(models.Model):
    """Model to store bus information"""
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100, unique=True)
    route = models.CharField(max_length=200, default="Unknown")
    capacity = models.IntegerField(default=50)
    driver_name = models.CharField(max_length=100, default="Unknown")
    driver_phone = models.CharField(max_length=15, default="Unknown")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.route}"


class Student(models.Model):
    """Model to store student profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='student_profile')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    place = models.CharField(max_length=150, blank=True, null=True)
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)
    roll_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.email})"


class BusEntry(models.Model):
    """Model to store bus entry and exit records"""
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='entries')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='bus_entries')
    boarding_place = models.CharField(max_length=200, blank=True, null=True)
    exit_place = models.CharField(max_length=200, blank=True, null=True)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=20, default='MANUAL')

    class Meta:
        ordering = ['-date', '-entry_time']
        verbose_name_plural = "Bus Entries"

    def __str__(self):
        return f"{self.student.name} - {self.bus.name} - {self.date}"
    
    def duration_in_bus(self):
        """Calculate time spent in bus"""
        if self.exit_time:
            return self.exit_time - self.entry_time
        return None

    def duration_minutes(self):
        duration = self.duration_in_bus()
        if duration:
            return int(duration.total_seconds() / 60)
        return None