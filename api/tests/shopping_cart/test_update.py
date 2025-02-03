import json
from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase

from api.enums.HttpHeaderContentType import HttpHeaderContentType


class UpdateShoppingCartTestCase(TestCase):
    fixtures: list[str] = ['user_with_shopping_cart.json']

    def test_update_shopping_cart_returns_method_not_allowed(self, ) -> None:
        response: HttpResponse = self.client.put(
            f'/api/shopping-cart/7/',
            json.dumps({
                'user_id': 17
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
