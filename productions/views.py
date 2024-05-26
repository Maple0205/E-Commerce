from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from common.serializers import CustomResponse
from productions.models import Production, ProductionItem
from productions.serializers import ProductionSerializer, ProductionItemSerializer, ProductionUpdateSerializer, ProductionItemUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.db.models import Q
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

authentication_header = openapi.Parameter('Authorization', in_=openapi.IN_HEADER, description="Bearer token for authentication", type=openapi.TYPE_STRING, required=True)
product_id = openapi.Parameter('product_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True)
page_id = openapi.Parameter('page_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True)
number_per_page = openapi.Parameter('number_per_page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True)
top_numbers_param = openapi.Parameter('top_numbers', openapi.IN_QUERY, description="Number of top products to retrieve", type=openapi.TYPE_INTEGER, required=True)
# class_grade = openapi.Parameter('class_grade', openapi.IN_QUERY, type=openapi.TYPE_STRING)
# standard = openapi.Parameter('standard', openapi.IN_QUERY, type=openapi.TYPE_STRING)
# size = openapi.Parameter('size', openapi.IN_QUERY, type=openapi.TYPE_STRING)
# plating = openapi.Parameter('plating', openapi.IN_QUERY, type=openapi.TYPE_STRING)
info = openapi.Parameter('info', openapi.IN_QUERY, type=openapi.TYPE_STRING)
category = openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_STRING)

# Create your views here.
class CreateProductionView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    @swagger_auto_schema(manual_parameters=[authentication_header], request_body=ProductionSerializer, operation_description='Only staff user can use this feature.')
    def post(self, request, *args, **kwargs):
        serializer = ProductionSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            res = {
                'id':obj.id,
                "name":obj.name,
                'status':obj.status,
            }
            data = CustomResponse.success(data=res)
            return Response(data, status=200)
        else:
            return Response(serializer.errors, status=400)

class UpdateProductionView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    @swagger_auto_schema(manual_parameters=[authentication_header], request_body=ProductionUpdateSerializer)
    def put(self, request, *args, **kwargs):
        product_id = request.data.get('id')
        product = get_object_or_404(Production, id=product_id)
        serializer = ProductionUpdateSerializer(product, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            res = {
                'id':obj.id,
                "name":obj.name,
                'status':obj.status,
            }
            data = CustomResponse.success(data=res)
            return Response(data, status=201)
        else:
            return Response(serializer.errors, status=400)
        
class CreateProductionItemView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    @swagger_auto_schema(manual_parameters=[authentication_header], request_body=ProductionItemSerializer, operation_description='Only staff user can use this feature.')
    def post(self, request, *args, **kwargs):
        serializer = ProductionItemSerializer(data=request.data)
        if serializer.is_valid():
            # validated_data = serializer.validated_data
            # product = Production.objects.get(id=validated_data['product'].id)
            # if product.single_item and product.items.all():
            #     return Response({'detail': 'This product is a Single model and already has an item, cannot create more.'}, status=status.HTTP_400_BAD_REQUEST)
            obj = serializer.save()
            res = {
                'id':obj.id,
                'status':obj.status,
            }
            data = CustomResponse.success(data=res)
            return Response(data, status=200)
        else:
            return Response(serializer.errors, status=400)

class UpdateProductionItemView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    @swagger_auto_schema(manual_parameters=[authentication_header], request_body=ProductionItemUpdateSerializer)
    def put(self, request, *args, **kwargs):
        product_item_id = request.data.get('id')
        product_item = get_object_or_404(ProductionItem, id=product_item_id)
        serializer = ProductionItemUpdateSerializer(product_item, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            res = {
                'id':obj.id,
                "sku":obj.sku,
                'status':obj.status,
            }
            data = CustomResponse.success(data=res)
            return Response(data, status=200)
        else:
            return Response(serializer.errors, status=400)
        
class GetProductionByIdView(APIView):
    @swagger_auto_schema(manual_parameters=[product_id])
    def get(self, request, *args, **kwargs):
        product_id = request.query_params.get('product_id')
        try:
            product = Production.objects.get(id=product_id)
            serializer = ProductionSerializer(product)
            data = CustomResponse.success(data=serializer.data)
            return Response(data, status=status.HTTP_200_OK)
        except Production.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
                   
class GetProductionsView(APIView):
    @swagger_auto_schema(manual_parameters=[page_id, number_per_page])
    def get(self, request, *args, **kwargs):
        page_id = int(request.query_params.get('page_id'))
        number_per_page = int(request.query_params.get('number_per_page'))
        try:
            products = Production.objects.all()[(page_id-1)*number_per_page:page_id*number_per_page]
            serializer = ProductionSerializer(products, many=True)
            data = CustomResponse.success(serializer.data)
            return Response(data, status=status.HTTP_200_OK)
        except Production.DoesNotExist:
            return Response({'detail': 'Products not found.'}, status=status.HTTP_404_NOT_FOUND)
         
class GetProductionsByFiltersView(APIView):
    @swagger_auto_schema(manual_parameters=[page_id, number_per_page, category])
    def get(self, request, *args, **kwargs):
        page_id = int(request.query_params.get('page_id'))
        number_per_page = int(request.query_params.get('number_per_page'))
        category = request.query_params.get('category')

        filter_kwargs = {
            'category': category,
        }
        filtered_kwargs = {k: v for k, v in filter_kwargs.items() if v is not None}
        try:
            products = Production.objects.filter(**filtered_kwargs)[(page_id-1)*number_per_page:page_id*number_per_page]
            serializer = ProductionSerializer(products, many=True)
            data = CustomResponse.success(serializer.data)
            return Response(data, status=status.HTTP_200_OK)
        except Production.DoesNotExist:
            return Response({'detail': 'Products not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class SearchProductionsView(APIView):
    @swagger_auto_schema(manual_parameters=[page_id, number_per_page, info])
    def get(self, request, *args, **kwargs):
        info = request.query_params.get('info')
        page_id = int(request.query_params.get('page_id'))
        number_per_page = int(request.query_params.get('number_per_page'))
        query = Q(name__icontains=info)
        try:
            products = Production.objects.filter(query)[(page_id-1)*number_per_page:page_id*number_per_page]
            serializer = ProductionSerializer(products, many=True)
            data = CustomResponse.success(serializer.data)
            return Response(data, status=status.HTTP_200_OK)
        except Production.DoesNotExist:
            return Response({'detail': 'Products not found.'}, status=status.HTTP_404_NOT_FOUND)

class TopProductionsView(APIView):
    @swagger_auto_schema(manual_parameters=[top_numbers_param])
    def get(self, request, *args, **kwargs):
        top_numbers = int(request.query_params.get('top_numbers'))
        try:
            products = Production.objects.all().order_by('-update_time')[:top_numbers]
            serializer = ProductionSerializer(products, many=True)
            data = CustomResponse.success(serializer.data)
            return Response(data, status=status.HTTP_200_OK)
        except Production.DoesNotExist:
            return Response({'detail': 'Products not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class GetCategoryListView(APIView):
    @swagger_auto_schema()
    def get(self, request, *args, **kwargs):
        data = Production.objects.values_list('category', flat=True).distinct()
        return Response(data, status=status.HTTP_200_OK)