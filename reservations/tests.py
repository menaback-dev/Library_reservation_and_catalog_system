from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from books.models import Book, Category
from reservations.models import Reservation

User = get_user_model()


class ReservationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Users
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='pass123')

        # Book setup
        self.category = Category.objects.create(name='Fiction')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            category=self.category,
            total_copies=2,
            available_copies=2
        )

        # Authenticate as testuser
        self.client.force_authenticate(user=self.user)

    def test_create_reservation_available(self):
        """Test reserving a book when copies are available."""
        url = reverse('reservation-list')
        data = {'book_id': self.book.id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'reserved')
        self.assertIsNone(response.data['queue_position'])

        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 1)

    def test_create_reservation_queued(self):
        """Test queuing when no copies are available."""
        # Another user reserves first → no copies left
        Reservation.objects.create(
            user=self.other_user,
            book=self.book,
            status='reserved'
        )
        self.book.available_copies = 0
        self.book.save()

        url = reverse('reservation-list')
        data = {'book_id': self.book.id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'queued')
        self.assertEqual(response.data['queue_position'], 1)

    def test_cancel_reserved_promotes_queue(self):
        """Test cancelling a reserved book promotes the first queued user."""
        # Create queued reservation (different user)
        queued_res = Reservation.objects.create(
            user=self.other_user,
            book=self.book,
            status='queued',
            queue_position=1
        )

        # Create reserved reservation for testuser
        res = Reservation.objects.create(
            user=self.user,
            book=self.book,
            status='reserved'
        )
        self.book.available_copies = 0
        self.book.save()

        # Cancel the reserved one
        url = reverse('reservation-detail', kwargs={'pk': res.id}) + 'cancel/'
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check promotion
        queued_res.refresh_from_db()
        self.assertEqual(queued_res.status, 'reserved')
        self.assertIsNone(queued_res.queue_position)

        # Check book copies returned
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 1)

        # Check original cancelled
        res.refresh_from_db()
        self.assertEqual(res.status, 'cancelled')
        self.assertIsNone(res.queue_position)
    
    def test_cancel_queued_shifts_positions(self):
        """Test cancelling a queued reservation shifts remaining positions."""
        # Create two queued items
        queued1 = Reservation.objects.create(
            user=self.other_user,
            book=self.book,
            status='queued',
            queue_position=1
        )
        queued2 = Reservation.objects.create(
            user=User.objects.create_user(username='user3', password='pass'),
            book=self.book,
            status='queued',
            queue_position=2
        )

        # Cancel the first queued
        url = reverse('reservation-detail', kwargs={'pk': queued1.id}) + 'cancel/'
        self.client.force_authenticate(user=self.other_user)  # switch to owner
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        queued2.refresh_from_db()
        self.assertEqual(queued2.queue_position, 1)  # should shift down