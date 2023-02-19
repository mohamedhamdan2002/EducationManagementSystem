from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'date_of_birth']

    def __str__(self):
        return self.username

    def get_last_submission(self, quiz = None):
        if quiz:
            last_time = max([obj.start_time for obj in self.submissions.filter(quiz=quiz)])
        else:
            last_time = max([obj.start_time for obj in self.submissions.all()])
        return self.submissions.get(start_time=last_time)