from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Book, UserModel, BookInfo, BorrowBooks, BookComment, RequestedBook
# Create your views here.


class GetMainBooks(APIView):
    pass


class FilterdBooks(APIView):
    pass


class SpecificInfoOfBook(APIView):
    pass


class LoveBook(APIView):
    pass


class BorrowBook(APIView):
    pass


class ReturnBook(APIView):
    pass


class UserBorrowedBook(APIView):
    pass


class RequestBook(APIView):
    pass


class RegisterNewBook(APIView):
    # Book 저장 -> book_info = book으로 관계 지으면 됨.
    def post(self, request):
        data = request.data
        isbn = data.get("isbn")
        book = Book(isbn=isbn)
        book.save()
        print(book)
        book_info = BookInfo(
            book=data.get("book"),
            title=data.get("title"),
            author=data.get("author"),
            thumbnail_image=data.get("thumbnail_image"),
            publisher=data.get("publisher"),
            page=data.get("page"),
            published_date=data.get("published_date"),
            keyword=data.get("keyword"),
            subtitle=data.get("subtitle"),
            description=data.get("description"),
            purchase_link=data.get("purchase_link")
        )
        book_info.save()
        return Response(status=200)


class RegisterRecommendBook(APIView):
    pass


class CheckBookPresentCondition(APIView):
    pass
