from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Appoint


class UserForm(UserCreationForm):
	first_name=forms.CharField()
	last_name=forms.CharField()
	email=forms.EmailField()

	class Meta():
		model = User
		fields=('first_name','last_name','email','password1','password2')
	
	def __init__(self,*args,**kwargs):
		super(UserCreationForm,self).__init__(*args,**kwargs)
		self.fields['password1'].help_text=''
		self.fields['password2'].help_text=''


class ProfileForm(forms.ModelForm):
	class Meta():
		model = Profile
		fields=('phone',)

class AppointForm(forms.ModelForm):
	class Meta():
		model = Appoint
		fields="__all__"

