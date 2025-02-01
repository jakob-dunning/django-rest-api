import json
from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase


class GetProductTestCase(TestCase):
    fixtures: list[str] = ['product.json']

    def test_get_product(self) -> None:
        response: HttpResponse = self.client.get('/api/product/5/')
        product_data: dict[str, str | int] = json.loads(response.content)

        self.assertDictEqual(
            product_data,
            {
                'id': 5,
                'manufacturer': 'NASA',
                'model': 'CX-77',
                'price': 30000,
                'category': 'PC'
            }
        )

    def test_get_product_with_non_existing_id_returns_not_found(self) -> None:
        response: HttpResponse = self.client.get('/api/product/99/')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
