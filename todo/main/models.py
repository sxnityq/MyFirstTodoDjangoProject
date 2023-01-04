from django.contrib.auth.models import (AbstractUser, BaseUserManager)
from django.db import models

from .utils import (get_profile_image_filepath,
                    get_user_default_profile_image)


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have email field")
        if not username:
            raise ValueError("Users must have username field")
        user = self.model(
            email=self.normalize_email(email),
            username=username, )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username=username,
                                email=email,
                                password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    username = models.CharField(primary_key=False, max_length=150, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    data_joined = models.DateTimeField(auto_now_add=True, verbose_name="date joined")
    email_verify = models.BooleanField(default=False)
    objects = CustomUserManager()
    profile_image = models.ImageField(upload_to=get_profile_image_filepath,
                                      blank=True, null=True,
                                      default=get_user_default_profile_image)

    def __str__(self):

        return self.username


class ToDoModels(models.Model):

    TaskId = models.AutoField(verbose_name='id', primary_key=True,
                              db_column='id', db_index=True)
    User = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users')
    TaskTitle = models.CharField(verbose_name='title', max_length=32, null=False,
                                 blank=False, unique=True)
    TaskText = models.TextField(verbose_name='description', max_length=4096, blank=True)
    Complete = models.BooleanField(verbose_name='is_complete', default=False)
    TimeOfCreation = models.DateTimeField(verbose_name='time_creation',
                                          auto_now_add=True)

    def __str__(self):

        return self.TaskTitle

    class Meta:

        db_table = 'Todo_table'
