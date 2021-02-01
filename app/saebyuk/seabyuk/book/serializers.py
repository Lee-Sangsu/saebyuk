from rest_framework import serializers
from ..models import Book, UserModel, BookInfo, BorrowBooks, BookComment, RequestedBook, RecommendedBook


class BorrowedBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model: BorrowBooks
        fields = ['book', 'borrowed_at', 'is_overdue']


class BookInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookInfo
        fields = '__all__'


class MainBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'registered_date']
