from django.contrib.auth.models import User

from training_system import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)


    class Meta:
        model = models.Product
        fields = '__all__'


class ProductCreateSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=100)
    cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    start_date = serializers.DateField(required=False)

    def create(self, validated_data):
        return models.Product.objects.create(**validated_data)


class SubscriptionSerializer(serializers.ModelSerializer):
    product = models.Product

    class Meta:
        model = models.Subscription
        fields = '__all__'

