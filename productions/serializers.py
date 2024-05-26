from rest_framework import serializers
from productions.models import Production, ProductionItem

class ProductionInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Production
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductionInfoSerializer, self).__init__(*args, **kwargs)
        self.fields.pop('is_delete')

class ProductionItemInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    product = ProductionInfoSerializer(read_only=True)

    class Meta:
        model = ProductionItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductionItemInfoSerializer, self).__init__(*args, **kwargs)
        self.fields.pop('is_delete')

class ProductionItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductionItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductionItemSerializer, self).__init__(*args, **kwargs)
        self.fields.pop('is_delete')

    # def validate(self, attrs):
    #     product = attrs.get('product')
    #     if product.single_item and ProductionItem.objects.filter(product=product).exists():
    #         raise serializers.ValidationError("This Production can only be associated with one Item.")
    #     return attrs

class ProductionSerializer(serializers.ModelSerializer):
    items = ProductionItemSerializer(many=True, read_only=True)
    related_products = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Production.objects.all(),
        required=False
    )
    
    class Meta:
        model = Production
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductionSerializer, self).__init__(*args, **kwargs)
        self.fields.pop('is_delete')

    def create(self, validated_data):
        related_products_data = validated_data.pop('related_products', [])
        product = Production.objects.create(**validated_data)
        product.related_products.set(related_products_data)
        return product
    

    # def update(self, instance, validated_data):
    #     related_products_data = validated_data.pop('related_products', None)
    #     instance.name = validated_data.get('name', instance.name)
        
    #     if related_products_data is not None:
    #         instance.related_products.set(related_products_data)
        
    #     instance.save()
    #     return instance
        
class ProductionUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=False)
    # description = serializers.CharField(required=False)
    # class_grade = serializers.CharField(required=False)
    # standard = serializers.CharField(required=False)
    # plating = serializers.CharField(required=False)
    status = serializers.IntegerField(required=False)
    # single_item = serializers.BooleanField(required=False)
    related_products = serializers.ListField(required=False)
    category = serializers.CharField(required=False)
    specification = serializers.JSONField(required=False)
    images = serializers.JSONField(required=False)
    sku = serializers.CharField(required=False)

    class Meta:
        model = Production
        fields = [
            'id',
            'name',
            # 'description',
            # 'class_grade',
            # 'standard',
            # 'plating',
            'status',
            # 'single_item',
            'related_products',
            'category',
            'specification',
            'images',
            'sku',
        ]

class ProductionItemUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    price = serializers.FloatField(required=False)
    promotion_price = serializers.FloatField(required=False)
    status = serializers.IntegerField(required=False)
    specification = serializers.JSONField(required=False, allow_null=True)
    sku = serializers.CharField(required=False)

    class Meta:
        model = ProductionItem
        fields = ['id', 'price', 'promotion_price', 'status', 'sku', 'specification']