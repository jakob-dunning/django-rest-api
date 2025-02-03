import json
from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase

from api.enums.HttpHeaderContentType import HttpHeaderContentType

SHOPPING_CART_POSITION_FIXTURE_ID: Final[int] = 5


class UpdateShoppingCartPositionTestCase(TestCase):
    fixtures: list[str] = ['user_with_shopping_cart_and_shopping_cart_position.json']

    def test_update_shopping_cart_position(self) -> None:
        new_product_data: dict[str, str | int] = {
            'amount': 3,
        }
        self.client.put(
            f'/api/shopping-cart-position/{SHOPPING_CART_POSITION_FIXTURE_ID}/',
            json.dumps(new_product_data)
        )
        response: HttpResponse = self.client.get(f'/api/shopping-cart-position/{SHOPPING_CART_POSITION_FIXTURE_ID}/')
        actual_product_data: dict[str, str | int] = json.loads(response.content)

        self.assertDictEqual(new_product_data | {'id': SHOPPING_CART_POSITION_FIXTURE_ID}, actual_product_data)

    def test_update_shopping_cart_position_with_non_positive_amount_returns_bad_request(self, ) -> None:
        response: HttpResponse = self.client.put(
            f'/api/shopping-cart-position/{SHOPPING_CART_POSITION_FIXTURE_ID}/',
            json.dumps({
                'amount': -7
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_shopping_cart_position_with_too_large_amount_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/shopping-cart-position/{SHOPPING_CART_POSITION_FIXTURE_ID}/',
            json.dumps({
                'amount': 14000
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_shopping_cart_position_with_missing_amount_returns_bad_request(self, ) -> None:
        response: HttpResponse = self.client.put(
            f'/api/shopping-cart-position/{SHOPPING_CART_POSITION_FIXTURE_ID}/',
            json.dumps({}),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_shopping_cart_position_with_unknown_attribute_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/shopping-cart-position/{SHOPPING_CART_POSITION_FIXTURE_ID}/',
            json.dumps({
                'amount': 8,
                'unknown_field': 'xyz'
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
