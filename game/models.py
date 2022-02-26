from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.tokens import default_token_generator
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=140, blank=True)
    avatar = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return str(self.user) + "Profile"


class Session:
    def __init__(self):
        pass

    def register(self, conf):
        error_message = "Error: "
        for (key, value) in conf.items():
            if key == "request":
                continue
            if not value or len(value) == 0:
                error_message += key + " can't be empty."
                return False, error_message

        if len(User.objects.filter(username=conf["username"])):
            error_message += "the username isn't available. Please try another."
            return False, error_message

        request = conf["request"]

        user = User.objects.create_user(
            username=conf["username"],
            password=conf["password"]
        )

        user.is_active = False
        user.save()


        return True, None