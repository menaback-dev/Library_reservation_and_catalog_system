from django.test import TestCase
from django.contrib.auth import get_user_model
from books.models import Book, Category
from reservations.models import Reservation
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class ReservationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.admin = User.objects.create_superuser(username='admin', password='admin123')
        
        self.category = Category.objects.create(name='Fiction')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            category=self.category,
            total_copies=2,
            available_copies=2
        )
        
        self.client.force_authenticate(user=self.user)

    def test_create_reservation_available(self):
        url = reverse('reservation-list')
        data = {'book_id': self.book.id}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'reserved')
        
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 1)

    def test_create_reservation_queued(self):
        # First reservation takes the last copy
        Reservation.objects.create(user=self.user, book=self.book, status='reserved')
        self.book.available_copies = 0
        self.book.save()
        
        url = reverse('reservation-list')
        data = {'book_id': self.book.id}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'queued')
        self.assertEqual(response.data['queue_position'], 1)

    def test_cancel_reserved_promotes_queue(self):
        # Create queued reservation first
        queued_res = Reservation.objects.create(
            user=User.objects.create_user(username='queueduser', password='pass'),
            book=self.book,
            status='queued',
            queue_position=1
        )
        
        # Create reserved one
        res = Reservation.objects.create(user=self.user, book=self.book, status='reserved')
        self.book.available_copies = 0
        self.book.save()
        
        url = reverse('reservation-detail', args=[res.id]) + 'cancel/'
        response = self.client.post(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        queued_res.refresh_from_db()
        self.assertEqual(queued_res.status, 'reserved')
        self.assertIsNone(queued_res.queue_position)