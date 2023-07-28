from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class CreateCustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        labels = {
            'username': _('Account Username'),
            'first_name': _('Name'),
            'email': _('Email ID'),
        }
