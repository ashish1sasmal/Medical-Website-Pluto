from django.shortcuts import render,redirect
from .forms import UserForm
from django.contrib.auth import authenticate
from .forms import ProfileForm,AppointForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Appoint,Booking
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.generic import TemplateView
import smtplib
from datetime import datetime, timedelta
from .models import Booking






def sent_email(rec_email,message):

		sender_email="canvashcode@gmail.com"
		password="etpfedmqbfiwmcye"
		now = datetime.now()
		dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
		message=message+"\ndate and time ="+str(dt_string)
		server=smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(sender_email,password)
		print("Login Success!")
		server.sendmail(sender_email,rec_email,message)
		print("Email has been sent to : ",rec_email)
class Homeview(TemplateView):
	template_name='patient/home.html'

class Aboutview(TemplateView):
	template_name='patient/about.html'

class Doctorview(TemplateView):
	template_name='patient/doctors.html'
	
@login_required(login_url='/login')
def appoint(request):

	if request.method=='POST':
		d=Booking.objects.filter()[:1].get()
		f=d.adate
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
		time=""
		adate=""

		if d.c1<50:
			d.c1+=1
			time="12:00 AM"
		elif d.c2<50:
			d.c2+=1
			time="6:00 PM"
		else:
			d.adate=(datetime.strptime(f, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
			time="12:00 AM"
			d.c1=1
			d.c2=0

		d.save()
		adate=d.adate
		appoint=Appoint(full_name=fullname,gender=gender,phone=phone,birth=birth,address=address,city=city,state=state,postal=postal,country=country,email=email,past_record=past_record,reason=reason,checkup=checkup,time=time,adate=adate)
		appoint.save()
		


		sent_email(email,"Your appointment is confirmed!\nYou will get appointment time and date in future.\nThank You")
		return redirect('app-success')
	return render(request,'patient/appointment.html',{'appointform':AppointForm})

class Success(TemplateView):
	template_name='patient/appointment_success.html'

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
				return redirect('home')
				
		else:
			messages.error(request,'Please Check your username and password !')
	return render(request,'patient/login.html')
	

