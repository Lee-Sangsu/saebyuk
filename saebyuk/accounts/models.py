from django.db import models
# Create your models here.


class UserModel(models.Model):
    kakao_id = models.IntegerField(unique=True)
    g_school_nickname = models.CharField(max_length=3, default='')
    kakao_nickname = models.CharField(max_length=20, default='')
    profile_image = models.CharField(max_length=20, default='')
    is_manager = models.BooleanField(default=False)
    objects = models.Manager()
    # 찜한 도서들 ForeignKey
