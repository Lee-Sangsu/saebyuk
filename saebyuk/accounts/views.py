from rest_framework.decorators import api_view
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from .models import User
import urllib
import requests
import os
import environ
env = environ.Env()
environ.Env.read_env()


class KakaoException(Exception):
    pass


# code 요청
def kakao_login(request):
    app_rest_api_key = env('KAKAO_CLIENT_ID')
    redirect_uri = "http://127.0.0.1:8000/account/login/kakao/callback"
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code")


# access token 요청
@api_view(['GET'])
def kakao_callback(request):
    # try:
    params = urllib.parse.urlencode(request.GET)
    app_rest_api_key = env('KAKAO_CLIENT_ID')
    redirect_uri = "http://127.0.0.1:8000/account/login/kakao/callback"
    user_token = request.GET.get("code")

    token_request = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={user_token}"
    )
    token_response_json = token_request.json()
    error = token_response_json.get("error", None)

    # if there is an error from token_request
    if error is not None:
        raise KakaoException()
    access_token = token_response_json.get("access_token")

    # post request
    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    kakao_id = profile_json.get("id")
    # print(kakao_id)
    # print(profile_json)

    # parsing profile json
    kakao_account = profile_json.get("kakao_account")

    profile = kakao_account.get("profile")
    nickname = profile.get("nickname")
    profile_image = profile.get("thumbnail_image_url")
    # 여기서 jwt 바로 뽑아내지 말고, kakao_id 같은 애 있는지 확인 한 담에 없으면 계정 생성하는 곳으로 리다이렉트 시키고, 이미 계정 있으면 token이랑 사용자 정보 리턴하면 됨. = try 부분에는 update, 유저 리턴, except 부분에는 그냥 redirect 시키기

    try:
        user_in_db = User.objects.get(kakao_id=kakao_id)
        data = {'code': user_token, 'access_token': access_token}
        accept = requests.post(
            f"http://127.0.0.1:8000/account/login/kakao/todjango/", data=data)
        accept_json = accept.json()
        # print(accept_json)
        accept_jwt = accept_json.get("key")

        user = User.objects.filter(kakao_id=kakao_id).update(
            kakao_nickname=nickname, profile_image=profile_image)
        return Response(user, status=201)
    except User.DoesNotExist:
        data = {'code': user_token, 'access_token': access_token}
        accept = requests.post(
            f"http://127.0.0.1:8000/account/login/kakao/todjango/", data=data
        )
        accept_json = accept.json()
        # print(accept_json)
        accept_jwt = accept_json.get("key")
        return Response(accept_jwt, status=200)
    # except:
    #     error_json = {'msg': 'Something Wrong from kakao'}
    #     return Response(error_json, status=401)


class KakaoToDjangoLogin(SocialLoginView):
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client
