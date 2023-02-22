from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name="homePage"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('store/', views.storePage, name='store')
]