from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartAddRequestSerializer, CartItemUpdateSerializer
from rest_framework import status
from productions.models import ProductionItem
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

authentication_header = openapi.Parameter('Authorization', in_=openapi.IN_HEADER, description="Bearer token for authentication", type=openapi.TYPE_STRING, required=True)

class ShowCartView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(manual_parameters=[authentication_header])
    def get(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

# @swagger_auto_schema(request_body=CartSerializer)
# class CreateCartView(APIView):
#     permission_classes = [IsAuthenticated]
#     @swagger_auto_schema(manual_parameters=[authentication_header])
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         cart, created = Cart.objects.get_or_create(user=user)
#         cart_data = CartSerializer(cart).data

#         if created:
#             return Response({"message": "Cart created successfully.", "cart": cart_data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "You already have a cart.", "cart": cart_data}, status=status.HTTP_201_CREATED)

class AddCartItemsView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        manual_parameters=[authentication_header],
        request_body=CartAddRequestSerializer,
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        items = request.data.get('items')
        if not items:
            return JsonResponse({'error': 'No items included.'}, status=status.HTTP_400_BAD_REQUEST)
        product_ids = [item.get('product_id') for item in items]
        if not all(ProductionItem.objects.filter(id=pid).exists() for pid in product_ids):
            return JsonResponse({'error': 'One or more product IDs are invalid.'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart, _ = Cart.objects.get_or_create(user=user)
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')
            product = ProductionItem.objects.get(id=product_id)

            CartItem.objects.update_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity},
            )
        cart_details = {
            'order_number': cart.order_number,
            'items': [
                {'product_id': item.product.id, 'quantity': item.quantity}
                for item in cart.items.all()
            ]
        }

        return JsonResponse({'message': 'Cart items added successfully.', 'cart': cart_details}, status=status.HTTP_200_OK)

class UpdateCartItemByIdView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(manual_parameters=[authentication_header], request_body=CartItemUpdateSerializer)
    def put(self, request, *args, **kwargs):
        user = request.user
        item_id = request.data.get('item_id')
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart = cart_item.cart

        if user != cart.user:
            return Response(
                {'error': 'You do not have permission to update this cart item.'},
                status=status.HTTP_403_FORBIDDEN
            )
        cart_item.quantity = request.data.get('quantity')
        if cart_item.quantity==0:
            cart_item.delete()
        else:
            cart_item.save()
        cart.save()
        cart_details = {
            'order_number': cart.order_number,
            'items': [
                {'product_id': item.product.id, 'quantity': item.quantity}
                for item in cart.items.all()
            ]
        }

        return JsonResponse({'message': 'Cart updated successfully.', 'cart': cart_details}, status=status.HTTP_200_OK)

