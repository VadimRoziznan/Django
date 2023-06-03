from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import ValidationError
from logistic. models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    title = serializers.CharField(max_length=60)

    class Meta:

        model = Product
        fields = '__all__'

    def validate(self, attrs):
        if attrs['title'] == Product.objects.get(title=attrs['title']).title:
            raise ValidationError(
                'такое уже есть'
            )
        return attrs


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
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for position in positions:
            s = StockProduct.objects.create(
                stock_id=stock.id,
                product_id=position.pop('product').id,
                price=position.pop('price'),
                quantity=position.pop('quantity')
            )
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

        for position in positions:
            stock_id = instance.id
            product_id = position.pop('product').id
            print(product_id)
            price = position.pop('price')
            quantity = position.pop('quantity')

            stock_product = StockProduct.objects.filter(
                stock_id=stock_id,
                product_id=product_id
            )

            stock_product.update(
                price=price,
                quantity=quantity
            )

        # stock_product = StockProduct.objects.filter()
        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock
