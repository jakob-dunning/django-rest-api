import json
from http import HTTPStatus
from typing import Final

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import models


@method_decorator(csrf_exempt, name='dispatch')
class ShoppingCartPosition(View):
    MUTABLE_PRODUCT_ATTRIBUTES: Final[set[str]] = {'amount'}

    def get(self, _, shopping_cart_position_id: int) -> JsonResponse:
        try:
            shopping_cart_position: models.ShoppingCartPosition = models.ShoppingCartPosition.objects.get(
                pk=shopping_cart_position_id)
            return JsonResponse(model_to_dict(shopping_cart_position))
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'Shopping cart position with id: {shopping_cart_position_id} not found'},
                                status=HTTPStatus.NOT_FOUND)

    def post(self, request: HttpRequest) -> JsonResponse:
        post_data: dict[str, int] = json.loads(request.body)

        if post_data.keys() != {'amount', 'product_id', 'shopping_cart_id'}:
            return JsonResponse(
                {'error': f'Missing or wrong attribute(s) for model shopping cart position'},
                status=HTTPStatus.BAD_REQUEST
            )

        try:
            product: models.Product = models.Product.objects.get(pk=post_data['product_id'])
        except ObjectDoesNotExist:
            return JsonResponse(
                {'error': f'Product with id: {post_data["product_id"]} not found'},
                status=HTTPStatus.NOT_FOUND
            )

        try:
            shopping_cart: models.ShoppingCart = models.ShoppingCart.objects.get(pk=post_data['shopping_cart_id'])
        except ObjectDoesNotExist:
            return JsonResponse(
                {'error': f'Shopping cart with id: {post_data["shopping_cart_id"]} not found'},
                status=HTTPStatus.NOT_FOUND
            )

        try:
            shopping_cart_position: models.ShoppingCartPosition = models.ShoppingCartPosition(
                product=product,
                shopping_cart=shopping_cart,
                amount=post_data['amount'],
            )
            shopping_cart_position.clean_fields()
            shopping_cart_position.save()
            return JsonResponse(model_to_dict(shopping_cart_position))
        except ValidationError as validation_error:
            return JsonResponse(validation_error.message_dict, status=HTTPStatus.BAD_REQUEST)

    def put(self, request: HttpRequest, shopping_cart_position_id: int) -> JsonResponse:
        try:
            put_data: dict[str, int] = json.loads(request.body)
            shopping_cart_position: models.ShoppingCartPosition = models.ShoppingCartPosition.objects.get(
                pk=shopping_cart_position_id)

            if put_data.keys() != {'amount'}:
                return JsonResponse({'error': f'Missing or wrong attribute(s) for model shopping cart position'},
                                    status=HTTPStatus.BAD_REQUEST)

            shopping_cart_position.amount = put_data['amount']
            shopping_cart_position.clean_fields()
            shopping_cart_position.save()
            return JsonResponse(model_to_dict(shopping_cart_position))
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'Shopping cart position with id: {shopping_cart_position_id} not found'},
                                status=HTTPStatus.NOT_FOUND)
        except ValidationError as validation_error:
            return JsonResponse(validation_error.message_dict, status=HTTPStatus.BAD_REQUEST)

    def delete(self, _, shopping_cart_position_id: int) -> JsonResponse:
        try:
            models.ShoppingCartPosition.objects.get(pk=shopping_cart_position_id).delete()
            return JsonResponse({}, status=HTTPStatus.NO_CONTENT)
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'Shopping cart position with id: {shopping_cart_position_id} not found'},
                                status=HTTPStatus.NOT_FOUND)
