from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer, OrderItemUpdateSerializer, OrderUpdateSerializer, OrderInfoSerializer, DeleteOrderItemSerializer
from .models import Order, OrderItem, StatusChoices
from rest_framework import status
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from common.serializers import CustomResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.mail import EmailMessage

authentication_header = openapi.Parameter('Authorization', in_=openapi.IN_HEADER, description="Bearer token for authentication", type=openapi.TYPE_STRING, required=True)
order_id = openapi.Parameter('order_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True)
info = openapi.Parameter('info', openapi.IN_QUERY, type=openapi.TYPE_STRING)
number_per_page = openapi.Parameter('number_per_page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True)
page_id = openapi.Parameter('page_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True)

# Create your views here.
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(manual_parameters=[authentication_header], request_body=OrderSerializer) 
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            obj = serializer.save()
            serialized_order = OrderSerializer(obj)
            # res = {
            #     'user':obj.user.id,
            #     'id':obj.id,
            #     "order_number":obj.order_number,
            #     'total_price':obj.total_price,
            #     'net_total_price': obj.net_total_price,
            #     'gst': obj.gst,
            #     'mobile':obj.mobile,
            #     'post_number':obj.post_number,
            #     'state':obj.state,
            #     'suburb':obj.suburb,
            #     'address':obj.address,
            #     'recipient_name':obj.recipient_name,
            #     'status':obj.status,
            #     'items': serialized_order.validated_data['items'],
            # }
            
            data = CustomResponse.success(data=serialized_order.data)
            return Response(data, status=200)
        else:
            return Response(serializer.errors, status=400)
  
class ShowOrdersByInfoView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(manual_parameters=[authentication_header, page_id, number_per_page, info])
    def get(self, request, *args, **kwargs):
        page_id = int(request.query_params.get('page_id'))
        number_per_page = int(request.query_params.get('number_per_page'))
        query = Q()
        user_id = request.query_params.get('user_id')
        if user_id:
            query &= Q(user=user_id)
        start_time = request.query_params.get('start_time')
        if start_time:
            start_time = parse_datetime(start_time)
            query &= Q(update_time__gte=start_time)
        end_time = request.query_params.get('end_time')
        if end_time:
            end_time = parse_datetime(end_time)
            query &= Q(update_time__lt=end_time)
        order_status = request.query_params.get('status')
        if order_status:
            query &= Q(status=order_status)
        orders = Order.objects.filter(query)[(page_id-1)*number_per_page:page_id*number_per_page]
        serializer = OrderInfoSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
  
class GetOrderByIdView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(manual_parameters=[authentication_header, order_id])
    def get(self, request, *args, **kwargs):
        order_id = request.query_params.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        
        serializer = OrderInfoSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(manual_parameters=[authentication_header], request_body=OrderUpdateSerializer) 
    def put(self, request, *args, **kwargs):
        order_number = request.data.get('order_number')
        order = get_object_or_404(Order, order_number=order_number)
        serializer = OrderUpdateSerializer(order, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            serialized_order = OrderSerializer(obj)

            status = request.data.get('status')
            if status:
                subject = "EEshopping Center order status updated!"
                email = request.user.email
                msg = StatusChoices(int(status)).label
                body = f"""
                <html>
                    <body>
                        <p>Hi {email},</p>
                        <p>Your order {obj.order_number} is {msg}.</p>
                        <p>To view your order details, click the link below:</p>
                        <a href="https://eesupply.com.au/">Go to EE_shopping</a>
                    </body>
                </html>
                """

                email_message = EmailMessage(
                    subject,
                    body,
                    'info@eesupply.com.au',
                    [email]
                )
                email_message.content_subtype = "html"
                num_sent = email_message.send()

                if not num_sent:
                    data = CustomResponse.error(data='Failed!')
                    return Response(data)

            data = CustomResponse.success(data=serialized_order.data)
            return Response(data, status=200)
        else:
            return Response(serializer.errors, status=400)

class UpdateOrderItemView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(manual_parameters=[authentication_header], request_body=OrderItemUpdateSerializer) 
    def put(self, request, *args, **kwargs):
      item_id = request.data.get('item_id')
      item = get_object_or_404(OrderItem, id=item_id)
      serializer = OrderItemUpdateSerializer(item, data=request.data)
      if serializer.is_valid():
          obj = serializer.save()
          res = {
              'price': obj.price,
              'order_number': obj.order.order_number,
              'item_id': obj.id,
              'quantity': obj.quantity,
          }
          data = CustomResponse.success(data=res)
          return Response(data, status=200)
      else:
          return Response(serializer.errors, status=400)
      
class DeleteOrderItemView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(manual_parameters=[authentication_header], request_body=DeleteOrderItemSerializer) 
    def delete(self, request, *args, **kwargs):
        item_id = request.data.get('item_id')
        try:
            item = OrderItem.objects.get(id=item_id)
            item.delete()
            return Response({'message': 'Order item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except OrderItem.DoesNotExist:
            return Response({'error': 'Order item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)