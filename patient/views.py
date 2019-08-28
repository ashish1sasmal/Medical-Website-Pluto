from django.shortcuts import render,redirect
from .forms import UserForm
from django.contrib.auth import authenticate
from .forms import ProfileForm,AppointForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Appoint
# Create your views here.
from django.views.generic import TemplateView

class Homeview(TemplateView):
	template_name='patient/home.html'

class Aboutview(TemplateView):
	template_name='patient/about.html'

class Doctorview(TemplateView):
	template_name='patient/doctors.html'
	
def appoint(request):
	if request.method=='POST':
		fullname=request.POST.get('fullname')
		gender=request.POST.get('gender')
		phone=request.POST.get('phone')
		birth=request.POST.get('birth')
		address=request.POST.get('address')
		city=request.POST.get('city')
		state=request.POST.get('state')
		postal=request.POST.get('postal')
		country=request.POST.get('country')
		email=request.POST.get('email')
		past_record=request.POST.get('past_record')
		reason=request.POST.get('reason')
		checkup=request.POST.get('checkup')
		appoint=Appoint(full_name=fullname,gender=gender,phone=phone,birth=birth,address=address,city=city,state=state,postal=postal,country=country,email=email,past_record=past_record,reason=reason,checkup=checkup)
		appoint.save()

		return redirect('home')
	return render(request,'patient/appointment.html',{'appointform':AppointForm})

class Achieveview(TemplateView):
	template_name='patient/achievements.html'

def register(request):
	if request.method=='POST':
		form = UserForm(data=request.POST)
		profile_form=ProfileForm(data=request.POST)
		if form.is_valid() and profile_form.is_valid():
			# recaptcha_response = request.POST.get('g-recaptcha-response')
			# data = {
   #              'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
   #              'response': recaptcha_response
   #              }
			# r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
			# result = r.json()
			# print(result['success'])
			# if result['success']:
			user=form.save(commit=False)
			user.username=form.cleaned_data.get('email')
			user.save()
			profile=profile_form.save(commit=False)
			profile.user=user
			profile.save()
			# name = form.cleaned_data.get('username')
			# user=form.save(commit=False)
			# user.username=name
			
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('login')
	else:
		form = UserForm()
		profile_form=ProfileForm()

	return render(request,'patient/register.html',{'form':form,'profile_form':profile_form})

def user_login(request):
	if request.method=='POST':
		email=request.POST.get('email')
		password=request.POST.get('password')
		print(email,password)
		user = authenticate(username=email, password=password)
		if user:
			if user.is_active:
				login(request, user)
				messages.success(request, f'You are logged in successfully!')
				
		else:
			messages.error(request,'Please Check your username and password !')
	return render(request,'patient/login.html')
	