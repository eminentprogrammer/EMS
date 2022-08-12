from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import ACCOUNT_TYPE, Account, Student

class RegistrationForm(UserCreationForm):
    username       = forms.CharField(label='', help_text="Student ID / Staff ID", widget=forms.TextInput(attrs={'class':'form-control','name':'username','placeholder':'User ID','autofocus':''}))
    email           = forms.EmailField(label='', max_length=254, help_text='Requried. School email address.', widget=forms.EmailInput(attrs={'class':'form-control border-0','name':'email','placeholder':'Email Address'}))
    password1       = forms.CharField(label='', help_text="Choose a strong password", widget=forms.PasswordInput(attrs={'class':'form-control','name':'password1','placeholder':'Password','autofocus':''}))
    password2       = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control', 'name':'password2', 'placeholder':'Confirm Password','autofocus':''}))
    account_type    = forms.ChoiceField(label='', choices=ACCOUNT_TYPE, help_text="Select Account Type")
    
    class Meta:
        model = Account
        fields = ('username','email','account_type', 'password1', 'password2')


class AccountAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(label='', max_length=254, widget=forms.EmailInput(attrs={'class':'form-control','name':'email','placeholder':'Email Address'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control','name':'password','placeholder':'Password'}))
    class Meta:
        model = Account
        fields = ('email', 'password')
		
    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid login")    


class ResetPasswordForm(forms.ModelForm):
    email = forms.EmailField(label='', max_length=254, widget=forms.EmailInput(attrs={'class':'form-control','name':'email','placeholder':'Email Address'}))
    class Meta:
        model = Account
        fields = ('email',)


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['gender','department','hall_of_residence','parent_name','parent_email','parent_phone_number']


class AccountUpdateForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ["lastname","firstname","phone_number"]