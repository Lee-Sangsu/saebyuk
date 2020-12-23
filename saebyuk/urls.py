"""saebyuk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from saebyuk.accounts.views import kakao_login, KakaoToDjangoLogin, kakao_sign_up

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('django.contrib.auth.urls')),
    path('account/', include('allauth.urls')),
    path('account/', include('rest_auth.urls')),
    path('account/registration/', include('rest_auth.registration.urls')),

    path('account/login/kakao/',
         kakao_login, name='kakao_sign_in'),
    path('account/sign-up/kakao/', kakao_sign_up, name="kakao_sign_up"),
    path('account/login/kakao/todjango/',
         KakaoToDjangoLogin.as_view(), name='kakao_todjango')
]
