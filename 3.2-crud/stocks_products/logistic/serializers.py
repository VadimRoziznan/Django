from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from logistic. models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    title = serializers.CharField(max_length=60)

    class Meta:

        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:

        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:

        model = Stock
        fields = '__all__'

    def create(self, validated_data):
        # print(validated_data)
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # for position in positions:
        #     print(position.pop('price'))
        # print(positions)
        # создаем склад по его параметрам

        stock = super().create(validated_data)
        # print(stock)
        for position in positions:
            # print(position.pop('product').id)
            s = StockProduct.objects.create(stock_id=stock.id, product_id=position.pop('product').id, price=position.pop('price'), quantity=position.pop('quantity'))
            s.save()

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock
