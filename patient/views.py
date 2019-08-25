from django.shortcuts import render
from .forms import UserForm
from .forms import ProfileForm
# Create your views here.
from django.views.generic import TemplateView

class Homeview(TemplateView):
	template_name='patient/home.html'

class Aboutview(TemplateView):
	template_name='patient/about.html'

class Doctorview(TemplateView):
	template_name='patient/doctors.html'
	

class Achieveview(TemplateView):
	template_name='patient/achievements.html'

def register(request):
	if request.method=='POST':
		form = UserForm(data=request.POST)
		profile_form=ProfileForm(data=request.POST)
		if form.is_valid() and profile_form.is_valid():
			recaptcha_response = request.POST.get('g-recaptcha-response')
			data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
                }
			r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
			result = r.json()
			print(result['success'])
			if result['success']:
				profile=profile_form.save()
				profile.save()
				name = form.cleaned_data.get('username')
				user=form.save(commit=False)
				user.username=name
				user.save()
				messages.success(request, f'Your account has been created! You are now able to log in')
				return redirect('login')
	else:
		form = UserForm()
		profile_form=ProfileForm()

	return render(request,'patient/register.html',{'form':form,'profile_form':profile_form})

class Loginview(TemplateView):
	template_name='patient/login.html'