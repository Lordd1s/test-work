from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from training_system import models, serializers


# Create your views here.
def home(request: Request) -> Response:
    return render(request, 'index.html')


class ProductCreateAPIView(APIView, LoginRequiredMixin):
    def post(self, request: Request) -> Response:
        serializer = serializers.ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(author=request.user)
                return Response(data={'success': 'Продукт успешно создан'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data={'error': 'Неверные данные'}, status=status.HTTP_400_BAD_REQUEST)


class GetProducts(APIView, LoginRequiredMixin):

    @swagger_auto_schema(
        operation_summary='Get products',
        responses={
            200: serializers.ProductSerializer,
            500: 'Internal Server Error'
        },
    )
    def get(self, request: Request) -> Response:
        try:
            subscribed = models.Subscription.objects.prefetch_related('product_id', 'user').filter(user=request.user)
            subs_serialized = serializers.SubscriptionSerializer(subscribed, many=True)

            all_products_to_buy = models.Product.objects.exclude(id__in=[sub.product_id.id for sub in subscribed])
            all_products_serial = serializers.ProductSerializer(all_products_to_buy, many=True)

            return Response(data={'subscribed': subs_serialized.data, 'available_to_buy': all_products_serial.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='POST',
    responses={
        201: 'Подписка успешно оформлена',
        500: 'Internal Server Error'
    }
)
@api_view(http_method_names=['POST'])
def subscribe(request: Request, pk: str) -> Response:
    """
    Подписка на продукт!

    params: pk(str): Принимает id продукта!
    """
    try:
        product = models.Product.objects.get(pk=int(pk))
        if product:
            models.Subscription.objects.create(
                user=request.user,
                product_id=product
            )
            return Response(data={'success': 'Подписка успешно оформлена'}, status=status.HTTP_201_CREATED)
        return Response(data={'error': 'Продукт не существует или удален'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
