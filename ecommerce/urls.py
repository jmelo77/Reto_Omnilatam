from django.urls import path
from ecommerce.views import *

app_name = 'ecommerce'

urlpatterns = [
    # Login
    path('login/client/', LoginView.as_view()),
    path('logout/client/', LogoutView.as_view()),

    # User
    path('create/client/', CreateClientView.as_view()),
    path('update/client/', UpdateClientView.as_view()),
    path('detail/client/<int:pk>/', DetailClientView.as_view()),
    path('list/client/', ListClientView.as_view()),
    path('delete/client/', DeleteClientView.as_view()),

    # Product
    path('create/product/', CreateProductView.as_view()),
    path('update/product/<int:pk>/', UpdateProductView.as_view()),
    path('detail/product/<int:pk>/', DetailProductView.as_view()),
    path('list/product/', ListProductView.as_view()),
    path('delete/product/<int:pk>/', DeleteProductView.as_view()),

    #Order
    path('create/order/',CreateOrder.as_view()),
    path('detail/order/<int:pk>/', DetailOrderView.as_view()),
    path('update/order/<int:pk>/', UpdateOrderView.as_view()),
    path('delete/order/<int:pk>/', DeleteOrderView.as_view()),

    #OrderProduct
    path('create/productorder/', CreateProductOrderView.as_view()),
    path('detail/productorder/<int:pk>/', DetailProductOrderView.as_view()),
    path('update/productorder/<int:pk>/', UpdateProductOrderView.as_view()),
    path('delete/productorder/<int:pk>/', DeleteProductOrderView.as_view()),

    #Payment
    path('create/payment/', CreatePaymentView.as_view()),
    path('detail/payment/<int:pk>/', DetailPaymentView.as_view()),
    path('update/payment/<int:pk>/', UpdatePaymentView.as_view()),
    path('delete/payment/<int:pk>/', DeletePaymentView.as_view()),
    
    # Shipping
    path('create/shipping/', CreateShippingView.as_view()),
    path('update/shipping/<int:pk>/', UpdateShippingView.as_view()),
    path('detail/shipping/<int:pk>/', DetailShippingView.as_view()),
    path('list/shipping/', ListShippingView.as_view()),
    path('delete/shipping/<int:pk>/', DeleteShippingView.as_view()),

    # Notification
    path('create/notification/', CreateNotificationView.as_view()),
    path('update/notification/<int:pk>/', UpdateNotificationView.as_view()),
    path('detail/notification/<int:pk>/', DetailNotificationView.as_view()),
    path('list/notification/', ListNotificationView.as_view()),
    path('delete/notification/<int:pk>/', DeleteNotificationView.as_view())    

]
