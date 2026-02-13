from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from .models import Category, Book
from .serializers import CategorySerializer, BookSerializer

User = get_user_model()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]  # Only admins manage categories

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'isbn']
    permission_classes = [IsAdminUser]  # CRUD for admins only
