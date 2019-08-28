
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('',views.Homeview.as_view(),name='home'),
    path('about/',views.Aboutview.as_view(),name='about'),
    path('doctors/',views.Doctorview.as_view(),name='doctors'),
    path('achievements/',views.Achieveview.as_view(),name='achieve'),
    path('register/',views.register,name='register'),
    path('appointments/',views.appoint,name='appointments'),
    path('login/',views.user_login,name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='patient/login.html'),name='logout'),
]
