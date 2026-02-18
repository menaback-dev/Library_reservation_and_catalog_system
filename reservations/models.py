from django.db import models
from django.conf import settings
from books.models import Book

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('reserved', 'Reserved'),
        ('queued', 'Queued'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),  # For future extension
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    reserved_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reserved')
    queue_position = models.PositiveIntegerField(null=True, blank=True)  # Null for reserved, set for queued

    class Meta:
        unique_together = ('user', 'book')  # One active reservation per user per book
        ordering = ['-reserved_at']

    def __str__(self):
        return f"{self.user} - {self.book.title} ({self.status})"