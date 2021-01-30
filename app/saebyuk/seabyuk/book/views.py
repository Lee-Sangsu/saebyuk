from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from ..models import Book, UserModel, BookInfo, BorrowBooks, BookComment, RequestedBook, RecommendedBook
from rest_framework.permissions import IsAuthenticated
from .serializers import MainBookSerializer, BookInfoSerializer
from datetime import datetime


class GetMainBooks(APIView):
    def get(self, request):
        no_filter_books = Book.objects.all().order_by('-id')[:6]
        no_filtered_books = MainBookSerializer(no_filter_books, many=True)
        # recommended_books = RecommendedBook.objects.latest()
        # for i in recommended_books.isbns:

        repsonse = {
            # "recommended_book": recommended_books,
            "no_filter_books": no_filtered_books.data}

        return Response(repsonse, status=200)


class FilterdBooks(APIView):
    def get(self, request):
        filter = request.data.get("filter")
        filtered_books = BookInfoSerializer(
            BookInfo.objects.filter(genre__contains=filter)).data  # annotate isbn 해야 해
        return Response(filtered_books, status=200)


class SpecificInfoOfBook(APIView):
    def get(self, request):
        isbn = request.data.get("isbn")
        book = Book.objects.get(isbn=isbn)
        book_info = BookInfoSerializer(
            BookInfo.objects.get(book=book)).data
        # book comment 나중에 추가.
        return Response(book_info, status=200)


class LoveBook(APIView):
    def post(self, request):
        # permission_class = [IsAuthenticated]
        g_nickname = request.data.get("g_school_nickname")
        user = UserModel.objects.get(g_school_nickname=g_nickname)
        isbn = request.data.get("isbn")
        book = Book.objects.filter(isbn=isbn)
        LoveBook(book=book, user=user).save()
        return Response("successfully written", status=200)


class BorrowBook(APIView):
    def post(self, request):
        # permission_class = [IsAuthenticated]
        user = UserModel.objects.get(
            g_school_nickname=request.data.get("g_school_nickname"))
        book = Book.objects.get(isbn=request.data.get("isbn"))
        BorrowBooks(book=book, user=user).save()
        return Response("successfully written", status=200)


class ReturnBook(APIView):
    def put(self, request):
        # permission_class = [IsAuthenticated]
        user = UserModel.objects.get(
            g_school_nickname=request.data.get("g_school_nickname"))
        book = Book.objects.get(isbn=request.data.get("isbn"))
        BorrowBooks.objects.filter(borrowed_at=request.data.get(
            "borrowed_at")).update(returned_at=datetime.now())
        return Response("successfully edited", status=200)


class UserBorrowedBook(APIView):
    def get(self, request):
        user = UserModel.objects.get(
            g_school_nickname=request.data.get("g_school_nickname"))
        borrowed_book = BorrowBooks.objects.filter(user=user, returned_at=None)
        return Response(borrowed_book, status=200)


class RequestBook(APIView):
    def post(self, request):
        user = UserModel.objects.get(
            g_school_nickname=request.data.get("g_school_nickname"))
        request_book = RequestedBook(
            user=user,
            book_title=request.data.get("book_title"),
            author=request.data.get("author"),
            interest_parts=request.data.get("interest_parts"),
            others=request.data.get("others")
        )
        request_book.save()
        return Response("successfully edited", status=200)


class RegisterNewBook(APIView):
    def post(self, request):
        # permission_class = [IsAuthenticated]  # is_manager로 구분해야 함.
        data = request.data.get("data")
        print(data)
        isbn = data.get("isbn")
        if Book.objects.filter(isbn=isbn).exists():
            return Response({"message": "해당 isbn을 지닌 책이 이미 있습니다."}, status=400)
        else:
            book = Book(isbn=isbn)
            book.save()
            print(book)
            book_info = BookInfo(
                book=book,
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
    def post(self, request):
        # permission_class = [IsAuthenticated]  # is_manager로 구분해야 함.
        data = request.data
        isbn = data.get("isbn")
        try:
            RecommendedBook(isbns=isbn).save()
            return Response({"message": "성공적으로 등록되었습니다."}, status=200)
        except:
            return Response({"해당 isbn을 지닌 책이 없습니다."}, status=400)


class CheckBookPresentCondition(APIView):
    pass
