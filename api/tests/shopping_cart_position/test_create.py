import json
from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase
from parameterized import parameterized

from api.enums.HttpHeaderContentType import HttpHeaderContentType
from api import models

VALID_PRODUCT_ID: Final[int] = 5
VALID_SHOPPING_CART_ID: Final[int] = 7
VALID_AMOUNT: Final[int] = 3

class CreateShoppingCartPositionTestCase(TestCase):
    fixtures = ['user_with_shopping_cart.json', 'product.json']

    def test_create_shopping_cart_position(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/shopping-cart-position/',
            json.dumps({
                'product_id': VALID_PRODUCT_ID,
                'shopping_cart_id': VALID_SHOPPING_CART_ID,
                'amount': VALID_AMOUNT
            }),
            content_type=HttpHeaderContentType.JSON
        )
        response_body = json.loads(response.content)

        shopping_cart_position: models.ShoppingCartPosition = models.ShoppingCartPosition.objects.get(pk=response_body['id'])

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(shopping_cart_position.product.id, VALID_PRODUCT_ID)
        self.assertEqual(shopping_cart_position.shopping_cart.id, VALID_SHOPPING_CART_ID)
        self.assertEqual(shopping_cart_position.amount, VALID_AMOUNT)

    def test_create_shopping_cart_position_with_non_existing_product_returns_not_found(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/shopping-cart-position/',
            json.dumps({
                'product_id': 999,
                'shopping_cart_id': VALID_SHOPPING_CART_ID,
                'amount': VALID_AMOUNT
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_shopping_cart_position_with_non_existing_shopping_cart_returns_not_found(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/shopping-cart-position/',
            json.dumps({
                'product_id': VALID_PRODUCT_ID,
                'shopping_cart_id': 999,
                'amount': VALID_AMOUNT
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_shopping_cart_position_with_non_positive_amount_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/shopping-cart-position/',
            json.dumps({
                'product_id': VALID_PRODUCT_ID,
                'shopping_cart_id': VALID_SHOPPING_CART_ID,
                'amount': 0
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_shopping_cart_position_with_too_large_amount_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/shopping-cart-position/',
            json.dumps({
                'product_id': VALID_PRODUCT_ID,
                'shopping_cart_id': VALID_SHOPPING_CART_ID,
                'amount': 10001
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    @parameterized.expand([
        [{
            'shopping_cart_id': VALID_SHOPPING_CART_ID,
            'amount': 3,
        }],
        [{
            'product_id': VALID_PRODUCT_ID,
            'amount': 3,
        }],
        [{
            'product_id': VALID_PRODUCT_ID,
            'shopping_cart_id': VALID_SHOPPING_CART_ID,
        }]
    ])
    def test_create_shopping_cart_position_with_missing_attribute_returns_bad_request(self, product_data) -> None:
        response: HttpResponse = self.client.post(
            '/api/shopping-cart-position/',
            json.dumps(product_data),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_shopping_cart_position_with_unknown_attribute_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/shopping-cart-position/',
            json.dumps({
                'product_id': VALID_PRODUCT_ID,
                'shopping_cart_id': VALID_SHOPPING_CART_ID,
                'amount': VALID_AMOUNT,
                'unknown_field': 'sdfsf'
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
