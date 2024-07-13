from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('add_subject/', views.add_subject, name='add_subject'),
    path('record_attendance/<int:subject_id>/<str:status>/', views.record_attendance, name='record_attendance'),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('subject/<int:subject_id>/edit/', views.edit_subject, name='edit_subject'),
    path('edit_attendance_record/<int:record_id>/', views.edit_attendance_record, name='edit_attendance_record'),
]
