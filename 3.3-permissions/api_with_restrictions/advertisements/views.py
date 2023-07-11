from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import AnonRateThrottle
from rest_framework.filters import SearchFilter, OrderingFilter

from advertisements.models import Advertisement, Favorite
from advertisements.serializers import AdvertisementSerializer, FavoriteSerializer
from advertisements.permissions import IsOwnerOrheadOnly
from advertisements.filters import AdvertisementFilter

from django_filters.rest_framework import DjangoFilterBackend


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrheadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AdvertisementFilter
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(creator=self.request.user)  # исключаем чужие черновики
        else:
            queryset = queryset.exclude(status='DRAFT')  # исключаем все черновики
        return queryset

    @action(detail=True, methods=["POST"], url_path='add-to-favorite', permission_classes=[IsAuthenticated])
    def add_to_favorite(self, request, pk=None):
        user_id = request.user
        favorite = Favorite.objects.filter(user_id=user_id, advertisement_id=pk)
        status = Advertisement.objects.filter(id=pk, status='OPEN')
        advertisement = Advertisement.objects.filter(id=pk, creator_id=user_id)

        if not advertisement and not favorite and status:
            Favorite.objects.create(user=user_id, advertisement_id=pk)
            return Response({"Response": "Add to favorite"})

        elif favorite:
            return Response({"Response": "Advertisement is already in favorites"})

        elif not status:
            return Response({"Response": "Advertisement status is closed or in draft."})
        return Response({"Response": "It is not possible to add to favorites, the post belongs to the author."})


    @action(detail=False, methods=["get"])
    def get_favorite(self, request, pk=None):
        user = request.user
        favorite = Favorite.objects.filter(user=user).select_related("advertisement")
        serializer = FavoriteSerializer(favorite, many=True)
        return Response(serializer.data)
