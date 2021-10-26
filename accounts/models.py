from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, fullName, address, password=None):
        user = self.model(
            email=self.normalize_email(email),
            fullName=fullName,
            address=address,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullName, address, password=None):
        user = self.create_user(
            email,
            fullName,
            address,
            password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    fullName = models.CharField(max_length=100)
    contactNo = models.CharField(blank=True, null=True, max_length=20)
    isSeller = models.BooleanField(default=False)
    isBuyer = models.BooleanField(default=False)
    address = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullName', 'address']

    def __str__(self):
        return self.fullName

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
