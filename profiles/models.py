from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, profile_name, password=None):
        email = self.normalize_email(email)
        user = self.model(email=email,
                          profile_name=profile_name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, profile_name, password):
        return self.create_user(email, profile_name, password)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    profile_name = models.CharField(max_length=50)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['profile_name']
