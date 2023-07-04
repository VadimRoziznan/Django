from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import AnonRateThrottle
from rest_framework.filters import SearchFilter, OrderingFilter

from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.permissions import IsOwnerOrheadOnly
from advertisements.filters import AdvertisementFilter

from django_filters.rest_framework import DjangoFilterBackend


class AdvertisementViewSet(ModelViewSet, ListAPIView, GenericAPIView):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwnerOrheadOnly]
    throttle_classes = [AnonRateThrottle]
    filter_backends = [
        DjangoFilterBackend, SearchFilter, OrderingFilter
    ]
    filterset_class = AdvertisementFilter
    filterset_fields = ['creator', 'status']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        creator = self.request.GET.get('creator')
        status = self.request.GET.get('status')
        response = Advertisement.objects.all().exclude(status='DRAFT') 
        if creator:
            response = Advertisement.objects.filter(creator_id=creator)
        if status:
            response = Advertisement.objects.filter(status=status)
        # if self.request.user.is_authenticated:
        #     queryset = queryset.filter(creator_id=self.request.user.id, status='DRAFT')  # исключаем чужие черновики
        #     return queryset
        # else:
        #     queryset = queryset.exclude(status='DRAFT')  # исключаем все черновики
        #     return queryset
        return response
