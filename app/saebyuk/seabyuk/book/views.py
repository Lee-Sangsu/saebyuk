from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Book, UserModel, BookInfo, BorrowBooks, BookComment, RequestedBook, RecommendedBook
from rest_framework.permissions import IsAuthenticated
from .serializers import MainBookSerializer,  BookInfoSerializer, BorrowedBooksSerializer
from datetime import datetime
from notion.client import NotionClient
from notion.block import TodoBlock, TextBlock, PageBlock
import json
import environ
env = environ.Env()
environ.Env.read_env()


class GetMainBooks(APIView):
    def get(self, request):
        no_filter_books = BookInfo.objects.all().order_by('-book__id')[:6]
        no_filtered_books = BookInfoSerializer(no_filter_books, many=True)
        # need to add 대출 가능 여부

        return Response(no_filtered_books.data, status=200)


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
            return Response("successfully written", status=200)


class ReturnBook(APIView):
    def put(self, request):
        # permission_class = [IsAuthenticated]
        data = request.data
        user = UserModel.objects.get(
            g_school_nickname=data.get("g_school_nickname"))
        book = Book.objects.get(isbn=data.get(
            "isbn")).update(borrow_available=True)
        BorrowBooks.objects.filter(book=book).filter(
            user=user).update(returned_at=datetime.now())
        return Response("successfully edited", status=200)


class UserBorrowedBook(APIView):
    def get(self, request, nickname):
        print(nickname)
        user = UserModel.objects.get(
            g_school_nickname=nickname)
        borrowed_book = BorrowBooks.objects.filter(
            user=user).filter(returned_at=None)
        serialized_borrowed_books = BorrowedBooksSerializer(
            borrowed_book, many=True)
        print(BorrowedBooksSerializer())
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
        # permission_class = [IsAuthenticated]  # is_manager로 구분해야 함.
        data = request.data.get("data")
        # print(data)
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
                genre=data.get("genre"),
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


@api_view(['POST'])
def faq(request):
    try:
        body = json.loads(request.body)
        data = body.get("data")

        title = data.get("title")
        text_body = data.get("body")

        # login
        token_v2 = f"{env('NOTION_TOKEN')}"
        client = NotionClient(token_v2=token_v2)

        # faq 페이지 URL
        url = f"{env('NOTION_PAGE_URL')}"
        page = client.get_block(url)

        new_page_block = page.children.add_new(PageBlock, title=title)
        gotten_new_page_block = client.get_block(new_page_block.id)
        gotten_new_page_block.children.add_new(TextBlock, title=text_body)
        return Response(data="good", status=200)

    except:
        return Response(data="sorry, we have a problem", status=400)
