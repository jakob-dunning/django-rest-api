import json
from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase

SHOPPING_CART_FIXTURE_ID: Final[int] = 7
INVALID_PRODUCT_ID: Final[int] = 99


class GetShoppingCartTestCase(TestCase):
    fixtures: list[str] = ['user_with_shopping_cart.json']

    def test_get_shopping_cart(self) -> None:
        response: HttpResponse = self.client.get(f'/api/shopping-cart/{SHOPPING_CART_FIXTURE_ID}/')
        product_data: dict[str, str | int] = json.loads(response.content)

        self.assertDictEqual(
            product_data,
            {
                'id': SHOPPING_CART_FIXTURE_ID
            }
        )

    def test_get_shopping_cart_with_non_existing_id_returns_not_found(self) -> None:
        response: HttpResponse = self.client.get(f'/api/shopping-cart/{INVALID_PRODUCT_ID}/')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
