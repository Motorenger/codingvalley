from django.db import IntegrityError
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
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

    @method_decorator(cache_page(60*60*48, key_prefix='reviews_viewset'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60*60*72, key_prefix='review_viewset'))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return ReviewSerializerForUpdate
        return ReviewSerializer

    def get_serializer_context(self):
        context = {}
        context["request"] = self.request
        return context


class ReviewLikeViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    queryset = ReviewLikes.objects.all()
    serializer_class = ReviewLikesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrIsAdminOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise Http404
