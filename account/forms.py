from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Entry

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]

class update(forms.ModelForm):
	class Meta:
		model = Entry
		fields = ["name", "Gasoline_type", "Gasoline", "date", "vehicle_number", "purpose"]

class CreateAdminForm(UserCreationForm):
	class Meta:
		model = User
		fields = '__all__'


