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


# class BookSerializer(serializers.ModelSerializer):
#     book_info = serializers.SerializerMethodField()

#     class Meta:
#         model = Book
#         fields = ['isbn', 'book_info', 'registered_date', 'borrow_available']

#     def get_book_info(self, obj):
#         data = BookInfoSerializer(
#             obj.objects.select_related('book').all(), many=True).data
#         return data


class BorrowedBooksSerializer(serializers.ModelSerializer):
    book = MainBookSerializer()
    # book_info = BookInfoSerializer(queryset=book)

    class Meta:
        model = BorrowBooks
        fields = ['book', 'borrowed_at', 'is_overdue']
