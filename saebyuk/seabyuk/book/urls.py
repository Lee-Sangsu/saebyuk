from django.urls import path, include
from .views import GetMainBooks, FilterdBooks, SpecificInfoOfBook, RegisterLoveBook, BorrowBook, ReturnBook, UserBorrowedBook, RequestBook, RegisterNewBook,  CheckBookPresentCondition, faq, SearchBook, GetUserLovedBooks, DeleteUserLovedBooks

urlpatterns = [
    path('main/', GetMainBooks.as_view()),
    path('filter/<str:filter>/', FilterdBooks.as_view()),
    path('info/<int:isbn>/', SpecificInfoOfBook.as_view()),
    path('love/', RegisterLoveBook.as_view()),
    path('love/not-anymore/', DeleteUserLovedBooks.as_view()),
    path('borrow/<int:isbn>/', BorrowBook.as_view()),
    path('return/', ReturnBook.as_view()),
    path('borrowed/<str:nickname>/', UserBorrowedBook.as_view()),
    path('love/<str:nickname>/', GetUserLovedBooks.as_view()),
    path('request/', RequestBook.as_view()),
    path('register/new/', RegisterNewBook.as_view()),
    path('search/<str:query>/', SearchBook.as_view()),
    path('present-condition/<str:nickname>/',
         CheckBookPresentCondition.as_view()),
    path("faq/", faq, name="faq")
]
