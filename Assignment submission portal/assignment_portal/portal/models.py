# portal/models.py
"""from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.TextField()
    admin = models.ForeignKey(User, related_name='assignments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending')
"""

# portal/models.py
from django.db import models

# User model
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# Assignment model
class Assignment(models.Model):
    user = models.ForeignKey(User, related_name='user_assignments', on_delete=models.CASCADE)  # User who submits the assignment
    task = models.TextField()
    admin = models.ForeignKey(User, related_name='admin_assignments', on_delete=models.CASCADE)  # Admin responsible for the assignment
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Compeleted', 'Compeleted'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending')
    file = models.FileField(upload_to='assignments/', null=True, blank=True)  # Add this line
    def __str__(self):
        return f"Assignment {self.id} - {self.user.username} -> {self.admin.username} ({self.status})"
