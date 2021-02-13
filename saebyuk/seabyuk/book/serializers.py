from rest_framework import serializers
from ..models import Book, UserModel, BookInfo, BorrowBooks, BookComment, LoveBook


class BookInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInfo
        fields = '__all__'


class MainBookSerializer(serializers.ModelSerializer):
    book_info = BookInfoSerializer()

    class Meta:
        model = Book
        fields = ['isbn', 'book_info', 'registered_date', 'borrow_available']


class BorrowedBooksSerializer(serializers.ModelSerializer):
    book = MainBookSerializer()

    class Meta:
        model = BorrowBooks
        fields = '__all__'


class LovedBooksSerializer(serializers.ModelSerializer):
    book = MainBookSerializer()

    class Meta:
        model = LoveBook
        fields = "__all__"
