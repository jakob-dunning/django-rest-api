import json
from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase

from api import models
from api.enums.HttpHeaderContentType import HttpHeaderContentType

USER_WITH_SHOPPING_CART_ID: Final[int] = 17
USER_WITHOUT_SHOPPING_CART_ID: Final[int] = 3


class CreateShoppingCartTestCase(TestCase):
    fixtures: list[str] = ['user.json', 'user_with_shopping_cart.json']

    def test_create_shopping_cart(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/shopping-cart/',
            {
                'user_id': USER_WITHOUT_SHOPPING_CART_ID
            },
            content_type=HttpHeaderContentType.JSON
        )
        response_body = json.loads(response.content)

        shopping_cart: models.ShoppingCart = models.ShoppingCart.objects.get(pk=response_body['id'])
        user: models.User = models.User.objects.get(pk=3)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(user.shopping_cart, shopping_cart)
        self.assertEqual(shopping_cart.user, user)

    def test_create_shopping_cart_with_non_existing_user_returns_not_found(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/shopping_cart/',
            {
                'user_id': 999
            },
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_shopping_cart_when_already_exists_returns_conflict(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/shopping-cart/',
            {
                'user_id': USER_WITH_SHOPPING_CART_ID
            },
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)

    def test_create_shopping_cart_with_missing_user_id_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/shopping-cart/',
            {},
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_shopping_cart_with_unknown_attribute_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/shopping-cart/',
            {
                'user_id': USER_WITHOUT_SHOPPING_CART_ID,
                'unknown_attribute': 'ksdfhu'
            },
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
