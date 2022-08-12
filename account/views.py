from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, Account, StudentProfileForm
from django.views.generic import View

from account.models import  Student

def dashboard_view(request):
	if not request.user.is_authenticated:
		return redirect("login")
	return render(request, "account/dashboard.html")



def create_profile(request, slug):
	user = Account.objects.get(slug=slug)
	form = StudentProfileForm()
	form2 = AccountUpdateForm()

	if request.POST:
		form = StudentProfileForm(request.POST)
		form2 = AccountUpdateForm(request.POST, instance=Account.objects.get(slug=slug))

		if form2.is_valid():
			form2.initial = {
					"lastname" 	: request.POST['lastname'],
					"firstname" 		: request.POST['firstname'],
					"phone_number" 	:request.POST['phone_number'],
			}
			form2.save()

		if form.is_valid():
			if not Student.objects.filter(user=Account.objects.get(slug=slug)).exists():
				student = Student.objects.create(user=Account.objects.get(slug=slug))
			form = StudentProfileForm(request.POST, instance=Student.objects.get(user=Account.objects.get(slug=slug)))

			form.initial = {
				"gender" : request.POST['gender'],
				"department" : request.POST['department'], 
				"hall_of_residence" : request.POST['hall_of_residence'], 
				"parent_name" : request.POST['parent_name'], 
				"parent_email" : request.POST['parent_email'], 
				"parent_phone_number" : request.POST['parent_phone_number'],
			}
			form.save()
			return redirect("dashboard_view")
	return render(request, "account/set_profile.html", locals())


def verify_email(request, slug):
	try:
		if request.user.is_authenticated:
			return redirect("dashboard_view")
	except Exception as e:
		pass
	if Account.objects.filter(slug=slug).exists():
		user = Account.objects.get(slug=slug)
		
		if not user.is_authenticated:
			if user.is_email_verified():
				return redirect("dashboard_view")

		if request.POST:
			pin = request.POST['verify-email']
			instance = Account.objects.get(slug=slug)
			if int(pin) == instance.email_verification_pin:
				instance.is_active = True
				instance.is_email_verified = True
				instance.save()
				if instance.account_type == 0:
					return redirect("create_profile", instance.slug)
				return redirect("dashboard_view")
	return render(request, 'account/management/verify-email.html')


def registration_view(request):
	form = RegistrationForm()
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			email = request.POST['email']
			username = request.POST['username']
			password = request.POST['password1']
			confirm_password = request.POST['password2']

			instance.save()

			instance.verify_email()
			
			return redirect("verify_email", instance.slug)
		else:
			raise ValidationError("Form is not valid")
	return render(request, 'account/register.html', locals())


def login_view(request): 
	form = AccountAuthenticationForm()
	if request.user.is_authenticated:
		return redirect("dashboard_view")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email 		= request.POST['email'].lower()
			password 	= request.POST['password']
			user 		= authenticate(email=email, password=password)

			if user:
				if user.is_active:
					login(request, user)
					return redirect("dashboard_view")
	return render(request, "account/login.html", locals())


def logout_view(request):
    logout(request)
    return redirect('/')


def account_view(request):    
	if not request.user.is_authenticated:
		return redirect("login")

	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)

		if form.is_valid():
			form.initial = {
					"parent_name" 	: request.POST['parent_name'],
					"parent_email" 		: request.POST['parent_email'],
					"parent_phone_no" 	:request.POST['parent_phone_no'],
			}
			form.save()
			success_message = f"{request.user.username}'s profile updated"
			return redirect("/")

	form = AccountUpdateForm(
		initial={
				"email": request.user.email, 
				"username": request.user.username,
			}
		)
	account_form = form
	return render(request, "account/account.html", locals())


def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})
