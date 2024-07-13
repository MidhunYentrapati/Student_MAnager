from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Subject, AttendanceRecord
from .forms import SubjectForm, AttendanceRecordForm

@login_required
def main_page(request):
    subjects = Subject.objects.filter(user=request.user)
    total_attendance = calculate_total_attendance(subjects)
    return render(request, 'attendance/main_page.html', {'subjects': subjects, 'total_attendance': total_attendance})

@login_required
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect('attendance:main_page')
    else:
        form = SubjectForm()
    return render(request, 'attendance/add_subject.html', {'form': form})

@login_required
def record_attendance(request, subject_id, status):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    now = timezone.now()
    # Create a new attendance record regardless of previous submissions on the same day
    AttendanceRecord.objects.create(subject=subject, status=status, date=now.date(), time=now.time())
    return redirect('attendance:main_page')

@login_required
def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    attendance_records = AttendanceRecord.objects.filter(subject=subject)
    total_present = attendance_records.filter(status='P').count()
    total_absent = attendance_records.filter(status='A').count()
    
    # Calculate the attendance status message
    target = subject.target_attendance
    actual = subject.attendance_percentage
    if actual >= target:
        periods_to_skip = int((total_present * (100 - target)) / target - total_absent)
        attendance_status_message = f"You can miss {periods_to_skip} periods and still meet your target."
    else:
        periods_needed = int(((target * (total_present + total_absent)) - (100 * total_present)) / (100 - target))
        attendance_status_message = f"You need to attend {periods_needed} more periods to meet your target."

    return render(request, 'attendance/subject_detail.html', {
        'subject': subject,
        'attendance_records': attendance_records,
        'total_present': total_present,
        'total_absent': total_absent,
        'attendance_status_message': attendance_status_message,
        'form': SubjectForm(instance=subject)
    })

@login_required
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('attendance:subject_detail', subject_id=subject.id)
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'attendance/edit_subject.html', {'form': form, 'subject': subject})

@login_required
def edit_attendance_record(request, record_id):
    record = get_object_or_404(AttendanceRecord, id=record_id, subject__user=request.user)
    subject = record.subject
    if request.method == 'POST':
        form = AttendanceRecordForm(request.POST, instance=record)
        if form.is_valid():
            if form.cleaned_data['status'] == 'D':
                record.delete()
            else:
                form.save()
            return redirect('attendance:subject_detail', subject_id=subject.id)
    else:
        form = AttendanceRecordForm(instance=record)
    return render(request, 'attendance/edit_attendance_record.html', {'form': form, 'record': record, 'subject': subject})

def calculate_total_attendance(subjects):
    total_present = sum(AttendanceRecord.objects.filter(subject=subject, status='P').count() for subject in subjects)
    total_absent = sum(AttendanceRecord.objects.filter(subject=subject, status='A').count() for subject in subjects)
    total_classes = total_present + total_absent
    return (total_present / total_classes * 100) if total_classes > 0 else 0
