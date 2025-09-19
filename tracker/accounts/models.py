from django.db import models
import uuid

# Create your models here.
class UserProfile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,unique=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} \t {self.email}"
