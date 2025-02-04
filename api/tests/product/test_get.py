import json
from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase

PRODUCT_FIXTURE_ID: Final[int] = 5
PRODUCT_FIXTURE_MANUFACTURER: Final[str] = 'NASA'
PRODUCT_FIXTURE_MODEL: Final[str] = 'CX-77'
PRODUCT_FIXTURE_PRICE: Final[int] = 30000
PRODUCT_FIXTURE_CATEGORY: Final[str] = 'PC'
INVALID_PRODUCT_ID: Final[int] = 99


class GetProductTestCase(TestCase):
    fixtures: list[str] = ['product.json']

    def test_get_product(self) -> None:
        response: HttpResponse = self.client.get(f'/api/product/{PRODUCT_FIXTURE_ID}/')
        product_data: dict[str, str | int] = json.loads(response.content)

        self.assertDictEqual(
            product_data,
            {
                'id': PRODUCT_FIXTURE_ID,
                'manufacturer': PRODUCT_FIXTURE_MANUFACTURER,
                'model': PRODUCT_FIXTURE_MODEL,
                'price': PRODUCT_FIXTURE_PRICE,
                'category': PRODUCT_FIXTURE_CATEGORY
            }
        )

    def test_get_product_with_non_existing_id_returns_not_found(self) -> None:
        response: HttpResponse = self.client.get(f'/api/product/{INVALID_PRODUCT_ID}/')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
