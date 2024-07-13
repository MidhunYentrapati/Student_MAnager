# todo/models.py
from django.db import models
from accounts.models import CustomUser

class Task(models.Model):
    STATUS_CHOICES = [
        ('U', 'Uncompleted'),
        ('P', 'In Progress'),
        ('F', 'Finished')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='U')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
