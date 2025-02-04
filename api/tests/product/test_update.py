import json
from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase
from parameterized import parameterized

from api.enums.HttpHeaderContentType import HttpHeaderContentType

VALID_PRODUCT_ID: Final[int] = 5
VALID_MANUFACTURER: Final[str] = 'Nasa'
VALID_MODEL: Final[str] = 'CX-77'
VALID_PRICE: Final[int] = 79900
VALID_CATEGORY: Final[str] = 'PC'

class UpdateProductTestCase(TestCase):
    fixtures: list[str] = ['product.json']

    def test_update_product(self) -> None:
        new_product_data: dict[str, str | int] = {
            'manufacturer': VALID_MANUFACTURER,
            'model': VALID_MODEL,
            'price': VALID_PRICE,
            'category': VALID_CATEGORY
        }
        self.client.put(
            f'/api/product/{VALID_PRODUCT_ID}/',
            json.dumps(new_product_data)
        )
        response: HttpResponse = self.client.get(f'/api/product/{VALID_PRODUCT_ID}/')
        actual_product_data: dict[str, str | int] = json.loads(response.content)

        self.assertDictEqual(new_product_data | {'id': VALID_PRODUCT_ID}, actual_product_data)

    def test_update_product_with_long_manufacturer_name_returns_bad_request(self, ) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{VALID_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': 'International Business Machines Corporation',
                'model': VALID_MODEL,
                'price': VALID_PRICE,
                'category': VALID_CATEGORY,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_empty_manufacturer_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{VALID_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': '',
                'model': VALID_MODEL,
                'price': VALID_PRICE,
                'category': VALID_CATEGORY,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_long_model_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{VALID_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': VALID_MANUFACTURER,
                'model': 'Microsoft Windows Vista Ultimate UPGRADE Limited Numbered Signature Blockchain Artifical Intelligence Edition',
                'price': VALID_PRICE,
                'category': VALID_CATEGORY,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_empty_model_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{VALID_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': VALID_MANUFACTURER,
                'model': '',
                'price': VALID_PRICE,
                'category': VALID_CATEGORY,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_negative_price_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{VALID_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': VALID_MANUFACTURER,
                'model': VALID_MODEL,
                'price': -5,
                'category': VALID_CATEGORY,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_high_price_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{VALID_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': VALID_MANUFACTURER,
                'model': VALID_MODEL,
                'price': 5000000,
                'category': VALID_CATEGORY,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_long_category_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{VALID_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': VALID_MANUFACTURER,
                'model': VALID_MODEL,
                'price': VALID_PRICE,
                'category': 'Blockchain Artificial Intelligence Cloud Crypto Software',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_empty_category_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{VALID_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': VALID_MANUFACTURER,
                'model': VALID_MODEL,
                'price': VALID_PRICE,
                'category': '',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    @parameterized.expand([
        [{
            'model': VALID_MODEL,
            'price': VALID_PRICE,
            'category': VALID_CATEGORY,
        }],
        [{
            'manufacturer': VALID_MANUFACTURER,
            'price': VALID_PRICE,
            'category': VALID_CATEGORY,
        }],
        [{
            'manufacturer': VALID_MANUFACTURER,
            'model': VALID_MODEL,
            'category': VALID_CATEGORY,
        }],
        [{
            'manufacturer': VALID_MANUFACTURER,
            'model': VALID_MODEL,
            'price': VALID_PRICE,
        }]
    ])
    def test_update_product_with_missing_attribute_returns_bad_request(self,
                                                                       product_data: dict[str, str | int]) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{VALID_PRODUCT_ID}/',
            json.dumps(product_data),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_unknown_attribute_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{VALID_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': VALID_MANUFACTURER,
                'model': VALID_MODEL,
                'category': VALID_CATEGORY,
                'price': VALID_PRICE,
                'unknown_field': 'xyz'
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
