from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'status', 'queue_position', 'reserved_at']
    list_filter = ['status', 'book__title']
    search_fields = ['user__username', 'book__title']