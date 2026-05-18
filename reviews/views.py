from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewListSerializer, ReviewDetailSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action

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

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my(self, request):
        """내가 작성한 리뷰 목록"""
        queryset = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReviewListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ReviewListSerializer(queryset, many=True)
        return Response(serializer.data)
    
# Create your views here.
