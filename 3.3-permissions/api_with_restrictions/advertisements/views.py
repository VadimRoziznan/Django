from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import AnonRateThrottle
from rest_framework.filters import SearchFilter, OrderingFilter

from advertisements.models import Advertisement, Favorite
from advertisements.serializers import AdvertisementSerializer, FavoriteSerializer
from advertisements.permissions import IsOwnerOrheadOnly
from advertisements.filters import AdvertisementFilter

from django_filters.rest_framework import DjangoFilterBackend


class AdvertisementViewSet(ModelViewSet, ListAPIView, GenericAPIView):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwnerOrheadOnly]
    throttle_classes = [AnonRateThrottle]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AdvertisementFilter
    filterset_fields = ["creator", "status"]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        creator = self.request.GET.get("creator")
        status = self.request.GET.get("status")

        if self.request.method == "DELETE":
            queryset = super().get_queryset()

        elif creator:
            if self.request.user.is_authenticated:
                queryset = super().get_queryset().filter(creator_id=creator)
            else:
                queryset = super().get_queryset().filter(creator_id=creator).exclude(status="DRAFT")

        elif status:
            if self.request.user.is_authenticated:
                queryset = super().get_queryset().filter(creator_id=self.request.user.id, status=status)
            else:
                queryset = super().get_queryset().filter(status=status).exclude(status="DRAFT")

        else:
            queryset = super().get_queryset().exclude(status="DRAFT")
        return queryset

    @action(detail=True, methods=["post"])
    def add_to_favorite(self, request, pk=None):
        advertisement_id = self.get_object().id
        user = request.user
        Favorite.objects.create(User=user, advertisement_id=advertisement_id)
        if Response.status_code == 200:
            return Response({"Status": "OK"})
        return Response({"Status": "bad request"})

    @action(detail=False, methods=["get"])
    def get_favorite(self, request, pk=None):
        user = request.user
        favorite = Favorite.objects.filter(User=user).select_related("advertisement")
        serializer = FavoriteSerializer(favorite, many=True)
        return Response(serializer.data)
