from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    sku = serializers.SerializerMethodField()
    # class_grade = serializers.SerializerMethodField()
    # standard = serializers.SerializerMethodField()
    # plating = serializers.SerializerMethodField()
    # size = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    sum_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = '__all__'
    
    def get_name(self, obj):
        return obj.product.product.name
    
    def get_sku(self, obj):
        return obj.product.sku
    
    # def get_class_grade(self, obj):
    #     return obj.product.product.class_grade
    
    # def get_standard(self, obj):
    #     return obj.product.product.standard

    # def get_plating(self, obj):
    #     return obj.product.product.plating

    # def get_size(self, obj):
    #     return obj.product.size
           
    def get_price(self, obj):
        return obj.product.promotion_price
    
    def get_sum_price(self, obj):
        return obj.product.promotion_price * obj.quantity
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_total_price(self, obj):
        return sum([item.product.promotion_price * item.quantity for item in obj.items.all()])

    
class CartItemAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)

class CartAddRequestSerializer(serializers.Serializer):
    items = CartItemAddSerializer(many=True, required=True)

class CartItemUpdateSerializer(serializers.Serializer):
    item_id = serializers.IntegerField(help_text="ID of the item to update")
    quantity = serializers.IntegerField(help_text="Quantity of the item", required=False)