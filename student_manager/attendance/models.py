from django.db import models
from accounts.models import CustomUser

class Subject(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_attendance = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    @property
    def attendance_percentage(self):
        total_present = AttendanceRecord.objects.filter(subject=self, status='P').count()
        total_absent = AttendanceRecord.objects.filter(subject=self, status='A').count()
        total = total_present + total_absent
        return ((total_present / total) * 100) if total > 0 else 0

    @property
    def total_present(self):
        return AttendanceRecord.objects.filter(subject=self, status='P').count()

    @property
    def total_absent(self):
        return AttendanceRecord.objects.filter(subject=self, status='A').count()

    def attendance_info(self):
        total = self.total_present + self.total_absent
        if total == 0:
            return "No attendance records yet."
        attendance_percentage = (self.total_present / total) * 100
        if attendance_percentage >= self.target_attendance:
            max_absent = (self.total_present * (100 / self.target_attendance)) - total
            return f"You can be absent for {int(max_absent)} more periods to maintain your target attendance."
        else:
            required_present = (self.target_attendance * total / 100) - self.total_present
            return f"You need to attend {int(required_present)} more periods to reach your target attendance."

class AttendanceRecord(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=1, choices=[('P', 'Present'), ('A', 'Absent')])
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.subject.name} - {self.date} - {self.status} - {self.time}"
