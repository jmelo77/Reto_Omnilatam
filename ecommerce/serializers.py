from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.core import exceptions
from ecommerce.helpers import get_or_none
from ecommerce.models import User, Product, Order, Shipping, ProductOrder, Payment, Notification

class ClientRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get("username", None)
        email = data.get("email", None)
        phone = data.get("phone", None)
        password = data.get("password", None)
        password_confirmation = data.get("password_confirmation", None)
        first_name = data.get("first_name", None)
        last_name = data.get("last_name", None)
        user = get_or_none(User, email=email)
        if user:
            msg = "This email already in use."
            raise exceptions.ValidationError(msg)
        if password != password_confirmation:
            msg = "Passwords do not match."

        else:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            email=email, phone=phone, password=password)
            user.save()
            data["user"] = user
        return data


class ClientUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        first_name = validated_data.get("first_name", '')
        last_name = validated_data.get("last_name", '')
        user = instance
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return instance


class UserClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'first_name', 'last_name')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                data["user"] = user
            else:
                msg = 'This username and password do not match.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Email and password must be sent.'
            raise exceptions.ValidationError(msg)
        return data


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price', 'quantity', 'tax', 'image', 'description', 'is_active')


# Order Serializers
class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('id', 'user_id', 'order_date', 'total', 'status')


class OrderReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user_id', 'order_date', 'total', 'status')


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)


#Product Order Serializers

class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        exclude = ('price')

class ProductOrderReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = '__all__'

class ProductOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        exclude = ('price',)

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ('user_id',)

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
