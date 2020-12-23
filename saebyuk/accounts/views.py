from django.core import serializers
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import renderer_classes, api_view
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from .models import UserModel
from .serializer import UserSerializer
import urllib
import requests
import os
import json
import environ
env = environ.Env()
environ.Env.read_env()


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def kakao_sign_up(request):
    body = json.loads(request.body)
    data = body.get("data")

    if UserModel.objects.filter(kakao_id=data.get("kakao_id")).exists():
        user_model = UserModel(
            kakao_id=data.get("kakao_id"),
            g_school_nickname=data.get("g_school_nickname"),
            kakao_nickname=data.get("kakao_nickname"),
            profile_image=data.get("profile_image"),
        )
        user_model.save()

        accept = requests.post(
            f"http://127.0.0.1:8000/account/login/kakao/todjango/", data={'access_token': data.get("access_token")})
        accept_json = accept.json()
        accept_jwt = accept_json.get("key")

        return Response(accept_jwt, status=201)
    else:
        return Response({"message": "User already exists"}, status=400)


# access token 받고 로그인
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def kakao_login(request):
    app_rest_api_key = env('KAKAO_CLIENT_ID')
    body = json.loads(request.body)
    data = body.get("data")
    access_token = data.get("access_token")

    # post request => 사용자 정보 가져오기
    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    kakao_id = profile_json.get("id")

    # parsing profile json
    kakao_account = profile_json.get("kakao_account")
    profile = kakao_account.get("profile")
    nickname = profile.get("nickname")
    # 카카오톡 프로필 이미지 등록하지 않은 경우, thumbnail_image_url, profile_image_url이 없음.
    profile_image = profile.get("thumbnail_image_url")

    try:
        # 가입된 사용자인 경우, jwt 제공
        user_in_db = UserModel.objects.get(kakao_id=kakao_id)
        print(user_in_db)
        data = {'access_token': access_token}
        accept = requests.post(
            f"http://127.0.0.1:8000/account/login/kakao/todjango/", data=data)
        accept_json = accept.json()
        accept_jwt = accept_json.get("key")
        # 사용자의 이미지가 변경된 경우, 사진 업데이트
        UserModel.objects.filter(kakao_id=kakao_id).update(
            kakao_nickname=nickname, profile_image=profile_image)
        serialized_user_info = UserSerializer(user_in_db, many=False)

        print(serialized_user_info.data)
        response = {'accept_jwt': accept_jwt,
                    'user': serialized_user_info.data}
        return Response(data=response, status=200)
    except UserModel.DoesNotExist:
        response = {'kakao_profile': profile,
                    'kakao_id': kakao_id, 'access_token': access_token}
        return Response(data=response, status=203)


class KakaoToDjangoLogin(SocialLoginView):
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client
