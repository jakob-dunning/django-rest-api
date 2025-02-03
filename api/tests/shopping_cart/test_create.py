import json
from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase

from api.enums.HttpHeaderContentType import HttpHeaderContentType
from api.models import ShoppingCart, User


class CreateShoppingCartTestCase(TestCase):
    fixtures: list[str] = ['user.json', 'user_with_shopping_cart.json']

    def test_create_shopping_cart(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/shopping-cart/',
            {
                'user_id': 3
            },
            content_type=HttpHeaderContentType.JSON
        )
        response_body = json.loads(response.content)

        shopping_cart: ShoppingCart = ShoppingCart.objects.get(pk=response_body['id'])
        user: User = User.objects.get(pk=3)

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
                'user_id': 17
            },
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)
