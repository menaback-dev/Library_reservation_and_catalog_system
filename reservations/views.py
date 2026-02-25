from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Max, F
from .models import Reservation
from .serializers import ReservationSerializer
from books.models import Book



class ReservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing book reservations.
    - Authenticated users can reserve books or join queue.
    - Cancel action promotes next in queue if applicable.
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()

    def get_queryset(self):
        return Reservation.objects.filter(
            user=self.request.user,
            status__in=['reserved', 'queued']
        )

    @transaction.atomic
    def perform_create(self, serializer):
        book = serializer.validated_data['book']

        if book.available_copies > 0:
            # Reserve immediately
            book.available_copies -= 1
            book.save(update_fields=['available_copies'])
            serializer.save(status='reserved')
        else:
            # Add to queue
            last_position = Reservation.objects.filter(
                book=book,
                status='queued'
            ).aggregate(Max('queue_position'))['queue_position__max']

            queue_position = (last_position or 0) + 1

            serializer.save(
                status='queued',
                queue_position=queue_position
            )

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        book = reservation.book

        if reservation.user != request.user:
            raise PermissionDenied("You can only cancel your own reservations.")

        if reservation.status == 'reserved':
            book.available_copies += 1
            book.save(update_fields=['available_copies'])

            
            next_in_queue = Reservation.objects.filter(
                book=book, status='queued'
            ).order_by('queue_position').first()

            if next_in_queue:
                next_in_queue.status = 'reserved'
                next_in_queue.queue_position = None
                next_in_queue.save(update_fields=['status', 'queue_position'])

        elif reservation.status == 'queued':
            pass  

        reservation.status = 'cancelled'
        reservation.queue_position = None
        reservation.save(update_fields=['status', 'queue_position'])

        
        queued_items = Reservation.objects.filter(
            book=book,
            status='queued'
        ).order_by('queue_position')

        for idx, item in enumerate(queued_items, start=1):
            if item.queue_position != idx:
                item.queue_position = idx
                item.save(update_fields=['queue_position'])

        return Response({'detail': 'Reservation cancelled successfully.'}, status=status.HTTP_200_OK)