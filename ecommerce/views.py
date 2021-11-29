from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from ecommerce.models import User, Product, Order, Shipping, ProductOrder, Payment, Notification
from ecommerce.serializers import ClientRegisterSerializer, ClientUpdateSerializer, UserClientSerializer, \
                                  Token, LoginSerializer, ProductSerializer, OrderCreateSerializer, \
                                  OrderReadSerializer, OrderUpdateSerializer, ProductOrderSerializer, \
                                  ProductOrderReadSerializer, ProductOrderUpdateSerializer, PaymentSerializer, \
                                  ShippingSerializer, NotificationSerializer    

# Create your views here.

# Login
class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user:
            token, created = Token.objects.get_or_create(user=user)
            serializer_user = UserClientSerializer(user)
            return Response({"token": token.key, "user": serializer_user.data}, status=200)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=204)


#User
class CreateClientView(APIView):

    def post(self, request):
        serializer = ClientRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        success = False
        code = 400
        if user:
            success = True
            code = 201
        return Response({"success": success}, status=code)


class UpdateClientView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_class = (TokenAuthentication)

    def post(self, request):
        user = request.user
        serializer_info = ClientUpdateSerializer(data=request.data)
        if serializer_info.is_valid(raise_exception=True):
            serializer_info.update(
                instance=user, validated_data=serializer_info.validated_data)
        serializer_user = UserClientSerializer(user)
        return Response({'user': serializer_user.data}, status=200)


class DetailClientView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = UserClientSerializer
    queryset = User.objects.filter(is_active=True)        


class ListClientView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = UserClientSerializer
    queryset = User.objects.filter(is_active=True).order_by('id')


class DeleteClientView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_class = (TokenAuthentication)
    serializer_class = UserClientSerializer

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.is_active = False
        user.save()
        return Response({'msg': "You have deactivated your account."}, status=200)


# Product
class CreateProductView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_class = (TokenAuthentication)
    serializer_class = ProductSerializer


class UpdateProductView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_class = (TokenAuthentication)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class DetailProductView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)


class ListProductView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True).order_by('id')


class DeleteProductView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_class = (TokenAuthentication)
    queryset = Product.objects.filter(is_active=True)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'msg': "deleted product."}, status=200)


# Order
class CreateOrder(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request):
        return Response({'msg': "Order created"}, status=201)


class DetailOrderView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = OrderReadSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class UpdateOrderView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = OrderUpdateSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class DeleteOrderView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user, is_active=True)
        return queryset

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'msg': "Deleted order."}, status=200)


# ProductOrder
class CreateProductOrderView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = ProductOrderSerializer

    def perform_create(self, serializer):
        print("serializer", serializer.validated_data)
        product = serializer.validated_data['product']
        order = serializer.validated_data['order']
        total_price_order_product = float(product.price) * \
            float(serializer.validated_data['quantity'])
        order.total_order = float(order.total_order) + \
            total_price_order_product
        serializer.save(price_per_unit=product.price,
                        total_price=total_price_order_product)


class DetailProductOrderView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = ProductOrderReadSerializer

    def get_queryset(self):
        queryset = ProductOrder.objects.filter(
            is_active=True, order__user=self.request.user)
        return queryset


class UpdateProductOrderView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = ProductOrderReadSerializer

    def get_queryset(self):
        queryset = ProductOrder.objects.filter(
            is_active=True, order__user=self.request.user)
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"order_product": serializer.data}, status=200)


class DeleteProductOrderView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)

    def get_queryset(self):
        queryset = ProductOrder.objects.filter(
            user=self.request.user, is_active=True)
        return queryset

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'msg': "successfully deleted."}, status=200)


class CreatePaymentView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        ids_order = serializer.validated_data['order_id']
        paid_value = serializer.validated_data['paid_value']
        for id_order in ids_order:
            if paid_value > 0 and id_order.total_order > 0:
                if id_order.total_order <= paid_value:
                    id_order.paid_value_order = id_order.total_order
                    paid_value = paid_value - id_order.total_order
                else:
                    id_order.total_order= id_order.total_order - paid_value
        serializer.save(user=self.request.user)


class UpdatePaymentView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_class = (TokenAuthentication)
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class DetailPaymentView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = PaymentSerializer
    queryset = Payment.objects.filter(is_active=True)


class ListPaymentView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = PaymentSerializer
    queryset = Payment.objects.filter(is_active=True).order_by('id')


class DeletePaymentView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_class = (TokenAuthentication)
    queryset = Payment.objects.filter(is_active=True)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'msg': "deleted product."}, status=200)


# Shipping
class CreateShippingView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_class = (TokenAuthentication)
    serializer_class = ShippingSerializer


class UpdateShippingView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_class = (TokenAuthentication)
    serializer_class = ShippingSerializer
    queryset = Shipping.objects.all()


class DetailShippingView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = ShippingSerializer
    queryset = Shipping.objects.filter(is_active=True)


class ListShippingView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = ShippingSerializer
    queryset = Shipping.objects.filter(is_active=True).order_by('id')


class DeleteShippingView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_class = (TokenAuthentication)
    queryset = Shipping.objects.filter(is_active=True)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'msg': "deleted product."}, status=200)
       
       
# Notification
class CreateNotificationView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_class = (TokenAuthentication)
    serializer_class = NotificationSerializer


class UpdateNotificationView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_class = (TokenAuthentication)
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()


class DetailNotificationView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = NotificationSerializer
    queryset = Notification.objects.filter(is_active=True)


class ListNotificationView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = ShippingSerializer
    queryset = Notification.objects.filter(is_active=True).order_by('id')


class DeleteNotificationView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_class = (TokenAuthentication)
    queryset = Notification.objects.filter(is_active=True)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'msg': "deleted product."}, status=200)       