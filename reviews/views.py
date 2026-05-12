from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewListSerializer, ReviewDetailSerializer
from .permissions import IsOwnerOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['movie', 'user', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializer
        return ReviewDetailSerializer

    def get_queryset(self):
        return Review.objects.select_related('user', 'movie').annotate(
            #like_count=Count('likes', distinct=True),
            #comment_count=Count('comments', distinct=True)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# Create your views here.
