from rest_framework import serializers
from ..models import Book, UserModel, BookInfo, BorrowBooks, BookComment, RequestedBook, RecommendedBook


class BorrowedBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model: BorrowBooks
        fields = ['book', 'borrowed_at', 'is_overdue']


class MainBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'registered_date', 'borrow_available']


class BookInfoSerializer(serializers.ModelSerializer):
    book = MainBookSerializer()

    class Meta:
        model = BookInfo
        fields = '__all__'
