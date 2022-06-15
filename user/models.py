from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def __str__(self):
        return f"username: {self.username} - fullname: {self.full_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
