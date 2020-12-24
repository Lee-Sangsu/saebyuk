from django.db import models
from ..account.models import UserModel


class Book(models.Model):
    isbn = models.IntegerField(unique=True)
    # https://docs.djangoproject.com/en/3.1/ref/forms/widgets/#django.forms.DateTimeInput 포맷으로 인풋
    registered_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'book'
        ordering = ['isbn']


class BookInfo(models.Model):
    # https://brunch.co.kr/@ddangdol/10 로 쿼리
    # https://developers.kakao.com/docs/latest/ko/daum-search/dev-guide#search-book api
    book_info = models.OneToOneField(
        Book, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=50)
    author = models.ArrayField()
    thumbnail_image = models.CharField(max_length=200)
    publisher = models.CharField(max_length=25)
    page = models.IntegerField()
    published_date = models.DateTimeField()
    keyword = models.ArrayField()
    subtitle = models.CharField(max_length=25)
    description = models.CharField(max_length=100)
    purchase_link = models.CharField(max_length=200)

    class Meta:
        db_table = 'book_info'


class BorrowBooks(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='borrower')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='book')
    borrowed_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True)
    is_overdue = models.BooleanField(default=False)

    class Meta:
        db_table = 'book_present_condition'


class BookComment(models.Model):
    # from django.db.models import Avg
    # >>> Book.objects.all().aggregate(Avg('price')) 로 별점 평균 구하라
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='commenter')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='book')
    rating = models.DemicalField(max_digits=2, demical_places=1, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=20)

    class Meta:
        db_table = 'book_comment'


class RecommendedBook(models.Model):
    pass


class RequestedBook(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=25)
    author = models.CharField(max_length=25)
    interest_parts = models.CharField(max_length=25)
    others = models.CharField(max_length=30)
