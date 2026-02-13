from rest_framework import serializers
from .models import Category, Book

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'category', 'category_id',
                 'total_copies', 'available_copies', 'cover_image_url']
        read_only_fields = ['available_copies']