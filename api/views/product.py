import json
from http import HTTPStatus
from typing import Final

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from api import models


@method_decorator(csrf_exempt, name='dispatch')
class Product(View):
    MUTABLE_PRODUCT_ATTRIBUTES: Final[set[str]] = {'manufacturer', 'model', 'price', 'category'}

    def get(self, _, product_id: int) -> JsonResponse:
        try:
            product: models.Product = models.Product.objects.get(pk=product_id)
            return JsonResponse(model_to_dict(product))
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'Product with id: {product_id} not found'}, status=HTTPStatus.NOT_FOUND)

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            post_data: dict[str,str|int] = json.loads(request.body)

            differing_keys: set[str] = self._get_diff_of_input_keys_and_mutable_product_keys(post_data)
            if len(differing_keys) > 0:
                return JsonResponse({'error': f'Missing or wrong attribute(s) for model product: {differing_keys}'},
                                    status=HTTPStatus.BAD_REQUEST)

            product: models.Product = models.Product(
                manufacturer=post_data.get('manufacturer'),
                model=post_data.get('model'),
                price=post_data.get('price'),
                category=post_data.get('category'),
            )
            product.clean_fields()
            product.save()
            return JsonResponse(model_to_dict(product))
        except ValidationError as validation_error:
            return JsonResponse(validation_error.message_dict, status=HTTPStatus.BAD_REQUEST)

    def put(self, request: HttpRequest, product_id: int) -> JsonResponse:
        try:
            put_data: dict[str,str|int] = json.loads(request.body)
            product: models.Product = models.Product.objects.get(pk=product_id)

            differing_keys: set[str] = self._get_diff_of_input_keys_and_mutable_product_keys(put_data)
            if len(differing_keys) > 0:
                return JsonResponse({'error': f'Missing or wrong attribute(s) for model product: {differing_keys}'},
                                    status=HTTPStatus.BAD_REQUEST)

            for key, value in put_data.items():
                setattr(product, key, value)
            product.clean_fields()
            product.save()
            return JsonResponse(model_to_dict(product))
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'Product with id: {product_id} not found'}, status=HTTPStatus.NOT_FOUND)
        except ValidationError as validation_error:
            return JsonResponse(validation_error.message_dict, status=HTTPStatus.BAD_REQUEST)

    def _get_diff_of_input_keys_and_mutable_product_keys(self, input_data: dict[str,str|int]) -> set[str]:
        return self.MUTABLE_PRODUCT_ATTRIBUTES.symmetric_difference(set(input_data.keys()))
