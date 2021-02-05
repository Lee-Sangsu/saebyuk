from rest_framework import serializers
from ..models import Book, UserModel, BookInfo, BorrowBooks, BookComment, RequestedBook, RecommendedBook


class MainBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'registered_date', 'borrow_available']


class BookInfoSerializer(serializers.ModelSerializer):
    book = MainBookSerializer()

    class Meta:
        model = BookInfo
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    book_info = serializers.RelatedField(
        source='book.book_info', read_only=True)

    class Meta:
        model = Book
        fields = ['isbn', 'book_info', 'registered_date', 'borrow_available']


class BorrowedBooksSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    # book_info = BookInfoSerializer(queryset=book)

    class Meta:
        model = BorrowBooks
        fields = ['book', 'borrowed_at', 'is_overdue']
