from django.db import models
# Create your models here.


class Book(models.Model):
    isbn = models.IntegerField(unique=True)
    # https://docs.djangoproject.com/en/3.1/ref/forms/widgets/#django.forms.DateTimeInput 포맷으로 인풋
    registered_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'book'
        ordering = ['isbn']


class UserModel(models.Model):
    kakao_id = models.IntegerField(unique=True)
    g_school_nickname = models.CharField(max_length=3, default='')
    kakao_nickname = models.CharField(max_length=20, default='')
    profile_image = models.CharField(max_length=200, default='')
    is_manager = models.BooleanField(default=False)
    # https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/ 로 쿼리하면 됨.
    love_book = models.ManyToManyField(Book, related_query_name='loved_book')
    objects = models.Manager()

    class Meta:
        db_table = 'users'
        ordering = ['kakao_id']


class BookInfo(models.Model):
    # https://brunch.co.kr/@ddangdol/10 로 쿼리
    # https://developers.kakao.com/docs/latest/ko/daum-search/dev-guide#search-book api
    book = models.OneToOneField(
        Book, on_delete=models.CASCADE, primary_key=True, related_query_name='book')
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    thumbnail_image = models.CharField(max_length=200)
    publisher = models.CharField(max_length=25)
    page = models.IntegerField()
    published_date = models.DateTimeField()
    keyword = models.CharField(max_length=30)
    subtitle = models.CharField(max_length=25)
    description = models.CharField(max_length=100)
    purchase_link = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'book_info'


class BorrowBooks(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_query_name='borrower')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_query_name='book')
    borrowed_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True)
    is_overdue = models.BooleanField(default=False)

    class Meta:
        db_table = 'book_present_condition'


class BookComment(models.Model):
    # from django.db.models import Avg
    # >>> Book.objects.all().aggregate(Avg('price')) 로 별점 평균 구하라
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_query_name='commenter')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_query_name='book')
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=20)

    class Meta:
        db_table = 'book_comment'


class RecommendedBook(models.Model):
    pass


class RequestedBook(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_query_name='requested_user')
    book_title = models.CharField(max_length=25)
    author = models.CharField(max_length=25)
    interest_parts = models.CharField(max_length=25)
    others = models.CharField(max_length=30)
