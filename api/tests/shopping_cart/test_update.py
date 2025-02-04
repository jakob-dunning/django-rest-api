import json
from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase

from api.enums.HttpHeaderContentType import HttpHeaderContentType

VALID_SHOPPING_CART_ID: Final[int] = 7
VALID_USER_ID: Final[int] = 7

class UpdateShoppingCartTestCase(TestCase):
    fixtures: list[str] = ['user_with_shopping_cart.json']

    def test_update_shopping_cart_returns_method_not_allowed(self, ) -> None:
        response: HttpResponse = self.client.put(
            f'/api/shopping-cart/{VALID_SHOPPING_CART_ID}/',
            json.dumps({
                'user_id': VALID_USER_ID
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
