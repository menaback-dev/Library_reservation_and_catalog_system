from rest_framework import serializers
from .models import Reservation
from books.models import Book               
from books.serializers import BookSerializer


class ReservationSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source='book',
        write_only=True,
        required=True,              
    )
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Reservation
        fields = [
            'id',
            'book',             
            'book_id',
            'reserved_at',
            'status',
            'queue_position',
            'user',
        ]
        read_only_fields = [
            'reserved_at',
            'status',
            'queue_position',
            'user',
        ]