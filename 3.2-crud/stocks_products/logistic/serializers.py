from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    title = serializers.CharField(max_length=60)

    class Meta:

        model = Product
        fields = '__all__'

    def validate(self, attrs):
        """
        Check for the existence of a product,
        if a product with the same name exists,
        we raise an exception.
        :param attrs: attributes for validation
        :return: returning attributes after validation
        """
        if attrs.get('title'):
            try:
                title = Product.objects.filter(title=attrs['title']).values()
                if len(title):
                    if attrs.get('title') == title.values()[0].get('title'):
                        raise ValidationError(
                            'Продукт с таким названием уже зарегистрирован.'
                        )
            except FileNotFoundError as error:
                print(error)
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
        """
        Create a new object in the database,
        modify related tables if necessary.
        :param validated_data: validated data
        :return: created database object
        """
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position in positions:
            create_product_in_stock = StockProduct.objects.create(
                stock_id=stock.id,
                product_id=position.pop('product').id,
                price=position.pop('price'),
                quantity=position.pop('quantity')
            )
            create_product_in_stock.save()

        return stock

    def update(self, instance, validated_data):
        """
        Updates the object in the database,
        if it does not exist, a new one is created.
        :param instance: object instance
        :param validated_data: validated data
        :return: updated or created database object.
        """
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for position in positions:
            stock_id = instance.id
            product_id = position.pop('product').id
            price = position.pop('price')
            quantity = position.pop('quantity')

            product = Product.objects.filter(id=product_id)
            stock_product = StockProduct.objects.filter(
                stock_id=stock_id,
                product_id=product_id
            )

            if product and not stock_product:
                create_product_in_stock = StockProduct.objects.create(
                    stock_id=stock.id,
                    product_id=product_id,
                    price=price,
                    quantity=quantity
                )
                create_product_in_stock.save()
            else:
                stock_product.update(
                    price=price,
                    quantity=quantity
                )
        return stock
