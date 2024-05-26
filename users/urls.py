"""
URL configuration for djangoProject2 project.
Sunmiao Ni
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('token/refresh/', views.CustomTokenRefreshView.as_view()),
    # path('token/verify/', TokenVerifyView.as_view()),
    path('sendvcode/', views.SendCode.as_view()),
    path('edit_profile/', views.EditProfile.as_view()),
    # path('loggg/', views.loggg),
    path('reset_password/', views.ResetPassword.as_view()),
    path('get_user_profile/', views.GetUserProfile.as_view()),
]
