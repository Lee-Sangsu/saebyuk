from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Book, UserModel, BookInfo, BorrowBooks, BookComment, RequestedBook, LoveBook
from rest_framework.permissions import IsAuthenticated
from .serializers import MainBookSerializer,  BookInfoSerializer, BorrowedBooksSerializer, LovedBooksSerializer
from datetime import datetime
from notion.client import NotionClient
from notion.block import TodoBlock, TextBlock, PageBlock
import json
import os
from django.db.models import Q


class GetMainBooks(APIView):
    def get(self, request):
        no_filter_books = Book.objects.all().order_by('-id')[:6]
        no_filtered_books = MainBookSerializer(no_filter_books, many=True)
        return Response(no_filtered_books.data, status=200)


class FilterdBooks(APIView):
    def get(self, request, filter):
        books = Book.objects.filter(book_info__genre__contains=[filter])
        filtered_books = MainBookSerializer(
            books, many=True).data
        return Response(filtered_books, status=200)


class SpecificInfoOfBook(APIView):
    def get(self, request):
        isbn = request.data.get("isbn")
        book = Book.objects.get(isbn=isbn)
        book_info = BookInfoSerializer(
            BookInfo.objects.get(book=book)).data
        # book comment 나중에 추가.
        return Response(book_info, status=200)


class RegisterLoveBook(APIView):
    def post(self, request):
        # permission_class = [IsAuthenticated]
        data = request.data.get("data")
        g_nickname = data.get("g_school_nickname")
        user = UserModel.objects.get(g_school_nickname=g_nickname)
        isbn = data.get("isbn")
        book = Book.objects.get(isbn=isbn)
        if LoveBook.objects.filter(book=book).filter(user=user).filter(loved=True).exists():
            return Response("Already Loved", status=400)
        else:
            loved_book = LoveBook(book=book, user=user, loved=True)
            loved_book.save()
            return Response("successfully written", status=200)


class DeleteUserLovedBooks(APIView):
    def put(self, request):
        data = request.data.get("data")
        loved_book_id = data.get("love_id")
        LoveBook.objects.filter(id=loved_book_id).update(loved=False)
        return Response("취소 성공", status=200)


class GetUserLovedBooks(APIView):
    def get(self, request, nickname):
        loved_books = LoveBook.objects.filter(
            user__g_school_nickname=nickname).filter(loved=True)
        serialized_data = LovedBooksSerializer(loved_books, many=True)
        return Response(serialized_data.data, status=200)


class BorrowBook(APIView):
    def post(self, request, isbn):
        # permission_class = [IsAuthenticated]
        try:
            data = request.data.get("data")
            user = UserModel.objects.get(
                g_school_nickname=data.get("g_school_nickname"))
            get_book_for_update = Book.objects.filter(isbn=isbn)
            get_book_for_update.update(borrow_available=False)

            get_book_for_borrow = Book.objects.get(isbn=isbn)
            borrow_book = BorrowBooks(book=get_book_for_borrow, user=user)
            borrow_book.save()

            return Response("successfully written", status=200)
        except:
            return Response("sry", status=400)


class ReturnBook(APIView):
    def put(self, request):
        # permission_class = [IsAuthenticated]
        try:
            data = request.data.get("data")
            print(data)
            user = UserModel.objects.get(
                g_school_nickname=data.get("g_school_nickname"))
            for i in data.get("isbn"):
                book = Book.objects.filter(
                    isbn=i).update(borrow_available=True)
                BorrowBooks.objects.filter(book=book).filter(
                    user=user).update(returned_at=datetime.now())
            return Response("successfully returned", status=200)
        except:
            return Response("sry", status=400)


class UserBorrowedBook(APIView):
    def get(self, request, nickname):
        # print(nickname)
        user = UserModel.objects.get(
            g_school_nickname=nickname)
        borrowed_book = BorrowBooks.objects.filter(
            user=user).filter(returned_at=None)
        serialized_borrowed_books = BorrowedBooksSerializer(
            borrowed_book, many=True)
        # print(BorrowedBooksSerializer())
        return Response(serialized_borrowed_books.data, status=200)


class RequestBook(APIView):
    def post(self, request):
        data = request.data.get("data")
        # print(data.get("g_school_nickname"))
        user = UserModel.objects.get(
            g_school_nickname=data.get("g_school_nickname"))
        request_book = RequestedBook(
            user=user,
            book_title=data.get("book_title"),
            author=data.get("author"),
            interest_parts=data.get("interest_parts"),
            others=data.get("others")
        )
        request_book.save()
        return Response("successfully registered", status=200)


class RegisterNewBook(APIView):
    def post(self, request):
        # permission_class = [IsAuthenticated]  # jwt로 구분해야 함.
        data = request.data.get("data")
        isbn = data.get("isbn")
        if Book.objects.filter(isbn=isbn).exists():
            return Response({"message": "해당 isbn을 지닌 책이 이미 있습니다."}, status=400)
        else:
            book_info = BookInfo(
                title=data.get("title"),
                author=data.get("author"),
                thumbnail_image=data.get("thumbnail_image"),
                publisher=data.get("publisher"),
                page=data.get("page"),
                published_date=data.get("published_date"),
                genre=data.get("genre"),
                keyword=data.get("keyword"),
                subtitle=data.get("subtitle"),
                description=data.get("description"),
                purchase_link=data.get("purchase_link")
            )
            book_info.save()
            book = Book(isbn=isbn, book_info=book_info)
            book.save()

            return Response(status=200)


class SearchBook(APIView):
    def get(self, request, query):
        try:
            search_res = Book.objects.filter(
                Q(book_info__title__contains=query) | Q(book_info__author__contains=query))
            serialized_book = MainBookSerializer(search_res, many=True)
            return Response(serialized_book.data, status=200)
        except:
            return Response({"해당 검색어의 책이 없습니다."}, status=400)


class CheckBookPresentCondition(APIView):
    def get(self, request, nickname):
        borrowed_book = BorrowBooks.objects.filter(
            user__g_school_nickname=nickname)
        serialized_borrowed_books = BorrowedBooksSerializer(
            borrowed_book, many=True)
        return Response(serialized_borrowed_books.data, status=200)


@api_view(['POST'])
def faq(request):
    try:
        body = json.loads(request.body)
        data = body.get("data")

        title = data.get("title")
        text_body = data.get("body")

        # login
        token_v2 = f"{os.environ.get('NOTION_TOKEN')}"
        client = NotionClient(token_v2=token_v2)

        # faq 페이지 URL
        url = f"{os.environ.get('NOTION_PAGE_URL')}"
        page = client.get_block(url)

        new_page_block = page.children.add_new(PageBlock, title=title)
        gotten_new_page_block = client.get_block(new_page_block.id)
        gotten_new_page_block.children.add_new(TextBlock, title=text_body)
        return Response(data="good", status=200)

    except:
        return Response(data="sorry, we have a problem", status=400)
