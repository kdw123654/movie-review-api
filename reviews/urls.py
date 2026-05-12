# reviews/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet
from comments.views import LikeToggleView 

router = DefaultRouter()
router.register('', ReviewViewSet, basename='review')

urlpatterns = [
    path('<int:review_id>/like/', LikeToggleView.as_view(), name='review-like'),
    path('', include(router.urls)),
]