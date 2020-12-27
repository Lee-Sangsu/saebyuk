from rest_framework import serializers
from ..models import Book, UserModel, BookInfo, BorrowBooks, BookComment, RequestedBook, RecommendedBook


class MainBookSerializer(serializers.ModelSerializer):
    book_info = BookInfoSerializer(many=False, read_only=True)

    class Meta:
        model = Book
        fields = ['isbn', 'registered_date', 'book_info']


class BookInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInfo
        fields = '__all__'
