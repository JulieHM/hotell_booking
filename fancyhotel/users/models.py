from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user, to be able to log in using email, and to store phone_number

    References:
        https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractbaseuser
        https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    phone_number = models.CharField(help_text="Maximum of 8 digits", max_length=8, blank=True, null=True)

    date_created = models.DateTimeField('Date of account creation', auto_now_add=True)

    # Flags:
    is_active = models.BooleanField(default=True)
        # NOTE: is_staff is used in combination with is_cleaner or is_investor
    is_staff = models.BooleanField('Works at the hotel', default=False)
    is_cleaner = models.BooleanField('Works as cleaner', default=False)
    is_investor = models.BooleanField('Has investor privileges', default=False)
        ### is_admin = models.BooleanField('Has admin privileges', default=False)


    # Set 'email' to be used as username
    USERNAME_FIELD = 'email'

    # Set 'email' to be used as email field
    EMAIL_FIELD = 'email'

    # Set which fields are required when creating a superuser
    REQUIRED_FIELDS = ['first_name', 'last_name',]


    def get_full_name(self):
        """Returns full name of user"""
        return F"{self.last_name}, {self.first_name}"

    def get_short_name(self):
        """Returns first name of user"""
        return self.first_name

    def __str__(self):
        """Returns email of user"""
        return self.get_username()

    
    class Meta:
        ordering = ['last_name', 'first_name']

    objects = CustomUserManager()
