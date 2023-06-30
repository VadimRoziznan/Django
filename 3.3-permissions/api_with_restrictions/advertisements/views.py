from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import AnonRateThrottle
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.permissions import IsOwnerOrheadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from advertisements.filters import AdvertisementFilter


class AdvertisementViewSet(ModelViewSet, ListAPIView):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrheadOnly]
    throttle_classes = [AnonRateThrottle]
    filter_backends = [
        DjangoFilterBackend, SearchFilter, OrderingFilter
    ]
    filterset_class = AdvertisementFilter
    # filterset_fields = ['creator_id']
    pagination_class = LimitOffsetPagination
    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        creator = self.request.GET.get('creator')
        response = Advertisement.objects.all()
        if creator:
            response = Advertisement.objects.filter(creator_id=creator)
        return response
