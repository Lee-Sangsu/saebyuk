from django.contrib import admin
from django.urls import path, include
from .saebyuk.account.views import kakao_login, KakaoToDjangoLogin, kakao_sign_up

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('django.contrib.auth.urls')),
    path('account/', include('saebyuk.account.urls')),
    path('book/', include('saebyuk.book.urls')),
]
