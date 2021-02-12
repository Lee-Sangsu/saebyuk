from rest_framework import serializers
from ..models import Book, UserModel, BookInfo, BorrowBooks, BookComment, RequestedBook


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
        fields = ['book', 'borrowed_at', 'is_overdue']
