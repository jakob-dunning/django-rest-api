import json
from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import models


@method_decorator(csrf_exempt, name='dispatch')
class ShoppingCart(View):
    def get(self, _, shopping_cart_id: int) -> JsonResponse:
        try:
            shopping_cart: models.ShoppingCart = models.ShoppingCart.objects.get(pk=shopping_cart_id)
            return JsonResponse(model_to_dict(shopping_cart))
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'Shopping cart with id: {shopping_cart_id} not found'},
                                status=HTTPStatus.NOT_FOUND)

    def post(self, request: HttpRequest) -> JsonResponse:
        post_data: dict[str, str | int] = json.loads(request.body)

        if post_data.keys() != {'user_id'}:
            return JsonResponse({'error': f'Missing user id or wrong attribute(s) for model product'},
                                status=HTTPStatus.BAD_REQUEST)

        try:
            user: models.User = models.User.objects.get(pk=post_data['user_id'])
        except ObjectDoesNotExist:
            return JsonResponse(
                {'error': f'User for id: {post_data["user_id"]} not found'},
                status=HTTPStatus.NOT_FOUND
            )

        if user.shopping_cart is not None:
            return JsonResponse(
                {'error': f'User with id: {post_data["user_id"]} already has a shopping cart'},
                status=HTTPStatus.CONFLICT
            )

        shopping_cart: models.ShoppingCart = models.ShoppingCart()
        user.shopping_cart = shopping_cart
        shopping_cart.save()
        user.save()
        return JsonResponse(model_to_dict(shopping_cart))

    def delete(self, _, shopping_cart_id: int) -> JsonResponse:
        try:
            shopping_cart: models.ShoppingCart = models.ShoppingCart.objects.get(pk=shopping_cart_id)
            user: models.User = shopping_cart.user
            user.shopping_cart = None
            user.save()
            shopping_cart.delete()

            return JsonResponse({}, status=HTTPStatus.NO_CONTENT)
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'Shopping cart with id: {shopping_cart_id} not found'},
                                status=HTTPStatus.NOT_FOUND)
