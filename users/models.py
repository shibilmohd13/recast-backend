from pyexpat import model
from statistics import mode
from urllib import request
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        if not email:
            raise ValueError("Users must have an email address")
        email=self.normalize_email(email),
        email = email[0]


        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,first_name, last_name, email, password=None):
        
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            first_name,
            last_name,
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique =True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()



    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self) :
        return self.email

class UserProfile(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE,null=True)
    api_usage = models.PositiveIntegerField(default=0)
    profile = models.ImageField(upload_to="profile_pic")

    def __str__(self) -> str:
        return f"{self.user.first_name}'s Profile"


@receiver(post_save, sender=UserAccount)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)



