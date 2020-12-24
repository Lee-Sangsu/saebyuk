from django.db import models
# Create your models here.
from ..book.models import Book


class UserModel(models.Model):
    kakao_id = models.IntegerField(unique=True)
    g_school_nickname = models.CharField(max_length=3, default='')
    kakao_nickname = models.CharField(max_length=20, default='')
    profile_image = models.CharField(max_length=200, default='')
    is_manager = models.BooleanField(default=False)
    # https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/ 로 쿼리하면 됨.
    love_book = models.ManyToManyField(Book)
    objects = models.Manager()

    class Meta:
        db_table = 'users'
        ordering = ['kakao_id']
