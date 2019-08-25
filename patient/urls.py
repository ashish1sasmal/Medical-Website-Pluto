
from django.urls import path
from . import views
urlpatterns = [
    path('',views.Homeview.as_view(),name='home'),
    path('about/',views.Aboutview.as_view(),name='about'),
    path('doctors/',views.Doctorview.as_view(),name='doctors'),
    path('achievements/',views.Achieveview.as_view(),name='achieve'),
    path('register/',views.Registerview.as_view(),name='register'),
    path('login/',views.Loginview.as_view(),name='login'),
]
