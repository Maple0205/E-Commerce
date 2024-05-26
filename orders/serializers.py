from rest_framework import serializers
from .models import Order, OrderItem
from productions.models import ProductionItem

class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        self.fields.pop('is_delete')

    def create(self, validated_data):
        user = self.context['request'].user
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data, user=user)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order,  **item_data)
        return order


class OrderItemUpdateSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(help_text="Price of each item", required=False)
    item_id = serializers.IntegerField(help_text="ID of the item to update")
    quantity = serializers.IntegerField(help_text="Quantity of the item", required=False)

    class Meta:
        model = Order
        fields = ['item_id', 'price', 'quantity']

class OrderUpdateSerializer(serializers.ModelSerializer):
    order_number = serializers.UUIDField()
    mobile = serializers.CharField(required=False)
    post_number = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    suburb = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    recipient_name = serializers.CharField(required=False)
    status = serializers.IntegerField(required=False)
    net_total_price = serializers.FloatField(required=False)
    gst = serializers.FloatField(required=False)
    total_price = serializers.FloatField(required=False)
    delivery_fee = serializers.FloatField(required=False)
    delivery_method = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = ['order_number', 'mobile', 'post_number', 'state', 'suburb', 'address', 'recipient_name', 'status', 'net_total_price', 'total_price', 'gst', 'delivery_fee', 'delivery_method']

class OrderItemInfoSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'

    def get_product(self, obj):
        product_id = obj.product.id
        product = ProductionItem.objects.get(id=product_id)
        res = {
            'id': product_id,
            'sku': product.sku,
            'name': product.product.name,
        }
        return res
    
class OrderInfoSerializer(serializers.ModelSerializer):
    items = OrderItemInfoSerializer(many=True)
    
    class Meta:
        model = Order
        fields = '__all__'

class DeleteOrderItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField(required=True)
