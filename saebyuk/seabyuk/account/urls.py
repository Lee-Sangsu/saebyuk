from django.urls import path, include
from .views import kakao_login, KakaoToDjangoLogin, kakao_sign_up

urlpatterns = [

    path('', include('allauth.urls')),
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),

    path('login/kakao/',
         kakao_login, name='kakao_sign_in'),
    path('sign-up/kakao/', kakao_sign_up, name="kakao_sign_up"),
    path('login/kakao/todjango/',
         KakaoToDjangoLogin.as_view(), name='kakao_todjango')
]
