from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user manager where email is the unique identifier instead of username.
    
    References:
        https://testdriven.io/blog/django-custom-user-model/
        https://github.com/django/django/blob/master/django/contrib/auth/base_user.py#L16
    """

    def create_user(self, email, password, **extra_fields):
        """Create and save a user with given email and password"""
        if not email:
            raise ValueError('The email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a superuser with given email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_cleaner', True)
        extra_fields.setdefault('is_investor', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        if extra_fields.get('is_cleaner') is not True:
            raise ValueError('Superuser must have is_cleaner = True')
        if extra_fields.get('is_investor') is not True:
            raise ValueError('Superuser must have is_investor = True')

        return self.create_user(email, password, **extra_fields)