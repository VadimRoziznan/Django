from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend, SearchFilter, OrderingFilter
    ]
    search_fields = ['title',]
    pagination_class = LimitOffsetPagination
    # при необходимости добавьте параметры фильтрации


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [
        DjangoFilterBackend, SearchFilter, OrderingFilter
    ]
    filterset_fields = ['products', ]
    # search_fields = ['address', ]
    # pagination_class = LimitOffsetPagination



    # при необходимости добавьте параметры фильтрации
