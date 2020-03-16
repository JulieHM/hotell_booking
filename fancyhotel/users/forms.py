from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Create a new CustomUser"""
    class Meta(UserCreationForm):
        model = CustomUser
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    """Change a CustomUser"""
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')