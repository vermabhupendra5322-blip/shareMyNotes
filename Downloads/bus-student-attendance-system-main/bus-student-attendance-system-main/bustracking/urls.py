from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/qr-code/<int:bus_id>/', views.generate_qr_code, name='qr_code'),
    path('admin/bus-report/<int:bus_id>/', views.bus_report, name='bus_report'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/board/', views.mark_boarding, name='mark_boarding'),
    path('student/exit/', views.mark_exit, name='mark_exit'),
    path('student/report/', views.student_report, name='student_report'),
    path('scan/<int:bus_id>/', views.scan_bus, name='scan_bus'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)