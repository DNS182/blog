from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class EmailField(forms.EmailField):

    def validate(self, value):
        super(forms.EmailField, self).validate(value)
        try:
            User.objects.get(email = value)
            raise forms.ValidationError("Email already exists")
        except User.MultipleObjectsReturned:
            raise forms.ValidationError("Email already exists")
        except User.DoesNotExist:
            pass



class UserRegForm(UserCreationForm):
    email = EmailField(required = True, label = 'Email')

    class Meta:
        model = User
        fields = ['username','email','password1' , 'password2']

    def email_validate(self):
        email = self.cleaned_data['email']
        femail = User.objects.get(email=email)
        if email in femail.exists():
            raise forms.ValidationError("EMAIL ALREADY TAKEN")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ( 'image' , )


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name' ,'last_name')