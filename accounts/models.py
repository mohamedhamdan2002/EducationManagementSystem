from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    date_of_birth = models.DateField()

    REQUIRED_FIELDS = ['email', 'date_of_birth']

    def __str__(self):
        return self.username

    def get_last_submission(self):
        last_time = max([obj.time for obj in self.submissions.all()])
        return self.submissions.get(time=last_time)