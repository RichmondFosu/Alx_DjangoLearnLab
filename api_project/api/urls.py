from django.urls import path, include
from .views import BookListListAPIView, BookViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'book_all', BookViewSet, basename='book_all')


urlpatterns = [
    # route for BookList view(ListAPIView)
    path('books/', BookListListAPIView.as_view(), name='book-list'), #maps to the BookList view

    # the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)), #this includes all routes registered with the router
]