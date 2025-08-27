from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('create-order/', views.CreateOrderView.as_view(), name='create_order'),
    path('order-history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('order-detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order-delete/<int:order_id>/', views.OrderDeleteView.as_view(), name='order_delete'),
]