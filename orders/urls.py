
from django.urls import path
from orders import views
urlpatterns = [
    path('create_order/', views.CreateOrderView.as_view()),
    path('get_orders_by_info/', views.ShowOrdersByInfoView.as_view()),
    path('get_order_by_id/', views.GetOrderByIdView.as_view()),
    path('update_order/', views.UpdateOrderView.as_view()),
    path('update_order_item/', views.UpdateOrderItemView.as_view()),
    path('delete_order_item/', views.DeleteOrderItemView.as_view()),
]
