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
from email.message import EmailMessage

from django.conf import settings




def sent_email(rec_email,sub,message,info):

		
		


		msg=EmailMessage()
		msg['Subject'] = sub
		msg['From'] = settings.EMAIL_HOST_USER
		msg['To'] = rec_email
		msg.set_content(f'{message}')
		password=settings.EMAIL_HOST_PASSWORD
		sender_email=settings.EMAIL_HOST_USER
		
		if info!={}:

			j=info['info']
			msg.add_alternative(f"""\
					<!doctype html>
	<html lang="en">
	  <head>
	    <!-- Required meta tags -->
	    <meta charset="utf-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

	    <!-- Bootstrap CSS -->
	    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	  

	    <title></title>
	  </head>
	  <body>
	    <div class="jumbotron"  >
	      <h1>Your Appointment has been confirmed on </h1>
	      <h2 ><i>Date : {j[0]} </i></h1>
	      <h2><i>Timings : {j[1]} </i></h1>
	       <h2><i>Test :  {j[2]}.</i></h1><br>
	       <h2><i>CheckUp Number : {j[6]}</i></h1>
	      <h3>Patient's Details : : </h2>
	      <h5>Name : {j[3]}</h5>
	      <h5>Gender : {j[4]}</h5>
	      <h5>DOB : {j[5]}</h5>
	    </div>

	    <!-- Optional JavaScript -->
	    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
	    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
	    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
	    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
	  </body>
	</html>
				""",subtype='html')
	
		now = datetime.now()
		dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
		message=message+"\ndate and time ="+str(dt_string)
		server=smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(sender_email,password)
		print("Login Success!")
		server.send_message(msg)
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
		e=0
		if d.c1<50:
			d.c1+=1
			e=d.c1
			time="12:00 AM"
		elif d.c2<50:
			d.c2+=1
			e=d.c2
			time="6:00 PM"
		else:
			d.adate=(datetime.strptime(f, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
			time="12:00 AM"
			d.c1=1
			d.c2=0
			e=d.c1

		d.save()
		adate=d.adate
		appoint=Appoint(full_name=fullname,gender=gender,phone=phone,birth=birth,address=address,city=city,state=state,postal=postal,country=country,email=email,past_record=past_record,reason=reason,checkup=checkup,time=time,adate=adate)
		appoint.save()
		
		info=f"Your Appointment has been fixed.\n For {checkup} and timings : {time} on {adate} ."

		sent_email(email,"Appointment Confirmation","Hello ashish",info={'info':[adate,time,checkup,fullname,gender,birth,e]})
		return render(request,'patient/success.html',{'info':info})
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
	

def contact(request):
	if request.method=='POST':
		name=request.POST.get('name')
		email=request.POST.get('email')
		subject=request.POST.get('subject')
		message=request.POST.get('message')

		sent_email('ashishsasmal1@gmail.com',"Message from patient",f"Name : {name}\nEmail : {email}\nSubject : {subject}\nMessage : {message}",{})

		
		info="Your message has been submited!"
		return render(request,'patient/success.html',{'info':info})
	return render(request,'patient/home.html')