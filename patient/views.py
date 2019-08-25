from django.shortcuts import render

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


