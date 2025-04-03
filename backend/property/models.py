from django.db import models
from user.models import User

class Property(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=50, blank=False, null=False)
    zip_code = models.CharField(max_length=10, blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else f"Property {self.id}"