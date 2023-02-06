from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from reviews.models import Review, ReviewLikes
from reviews.serializers import ReviewSerializer, ReviewSerializerForUpdate, ReviewLikesSerializer
from users.permissions import IsOwnerOrIsAdminOrReadOnly


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrIsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return ReviewSerializerForUpdate
        return ReviewSerializer


class ReviewLikeViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    queryset = ReviewLikes.objects.all()
    serializer_class = ReviewLikesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrIsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)