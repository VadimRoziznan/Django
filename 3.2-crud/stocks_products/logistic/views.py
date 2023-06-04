from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from logistic.models import Product, Stock, StockProduct
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend, SearchFilter, OrderingFilter
    ]
    search_fields = ['title',]
    pagination_class = LimitOffsetPagination


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [
        DjangoFilterBackend, SearchFilter, OrderingFilter
    ]
    filterset_fields = ['products', ]
    pagination_class = LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        context = []
        product_id = request.GET.get('products')
        stocks = Stock.objects.raw(
            '''
            SELECT 
                ls.id, address 
            FROM 
                logistic_stock ls 
            FULL JOIN 
                logistic_stockproduct ls2 
            ON 
                ls2.stock_id = ls.id 
            WHERE 
                product_id = %s;
            ''', [product_id])

        for stock in stocks:
            context.append(
                {
                    'id': stock.id,
                    'address': stock.address
                }
            )
        return Response(context)
