from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	
	phone=models.CharField(max_length=10)

	def __str__(self):
		return f'{self.user.username} Profile'

class Booking(models.Model):
	count=models.IntegerField()
	date=models.DateField()

class Appoint(models.Model):
	full_name=models.CharField(max_length=40)
	gender=models.CharField(max_length=20)
	phone=models.CharField(max_length=10)
	birth=models.DateField()
	address=models.CharField(max_length=50)
	city=models.CharField(max_length=30)
	state=models.CharField(max_length=30)
	postal=models.CharField(max_length=20)
	country=models.CharField(max_length=20)
	email=models.EmailField()
	past_record=models.BooleanField()
	reason=models.TextField()
	checkup=models.CharField(max_length=20)
