# # forms.py
# from django import forms
# from django.contrib.auth.models import User
# import re
# from .models import Foydalanuvchi

# class UserRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username','password']

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         # Add custom validation logic for usernames
#         if len(username) < 5:
#             raise forms.ValidationError("Username must be at least 5 characters long.")
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError("Username is already taken.")
#         return username

#     def clean_password(self):
#         password = self.cleaned_data['password']
#         # Add custom validation logic for passwords
#         if len(password) < 8:
#             raise forms.ValidationError("Password must be at least 8 characters long.")
#         if not any(char.isdigit() for char in password):
#             raise forms.ValidationError("Password must contain at least one digit.")
#         if not any(char.isalnum() for char in password):
#             raise forms.ValidationError("Password must contain at least one symbol.")
#         return password
