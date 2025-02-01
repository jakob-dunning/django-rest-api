import json
from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase
from parameterized import parameterized

from api.enums.HttpHeaderContentType import HttpHeaderContentType


class UpdateProductTestCase(TestCase):
    fixtures: list[str] = ['product.json']
    FIXTURE_PRODUCT_ID: Final[int] = 5

    def test_update_product(self) -> None:
        new_product_data: dict[str, str | int] = {
            'manufacturer': 'NASA',
            'model': 'CX-77',
            'price': 20000,
            'category': 'PC'
        }
        self.client.put(
            f'/api/product/{self.FIXTURE_PRODUCT_ID}/',
            json.dumps(new_product_data)
        )
        response: HttpResponse = self.client.get(f'/api/product/{self.FIXTURE_PRODUCT_ID}/')
        actual_product_data: dict[str, str | int] = json.loads(response.content)

        self.assertDictEqual(new_product_data | {'id': self.FIXTURE_PRODUCT_ID}, actual_product_data)

    def test_update_product_with_long_manufacturer_name_returns_bad_request(self, ) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{self.FIXTURE_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': 'International Business Machines Corporation',
                'model': 'PDP-11',
                'price': 30000,
                'category': 'PC',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_empty_manufacturer_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{self.FIXTURE_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': '',
                'model': 'PDP-11',
                'price': 30000,
                'category': 'PC',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_long_model_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{self.FIXTURE_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': 'Microsoft',
                'model': 'Microsoft Windows Vista Ultimate UPGRADE Limited Numbered Signature Blockchain Artifical Intelligence Edition',
                'price': 30000,
                'category': 'Software',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_empty_model_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{self.FIXTURE_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': 'Microsoft',
                'model': '',
                'price': 30000,
                'category': 'PC',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_negative_price_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{self.FIXTURE_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': 'Microsoft',
                'model': 'Windows',
                'price': -5,
                'category': 'Software',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_high_price_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{self.FIXTURE_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': 'Microsoft',
                'model': 'Windows',
                'price': 5000000,
                'category': 'Software',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_long_category_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{self.FIXTURE_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': 'Microsoft',
                'model': 'Windows',
                'price': 30000,
                'category': 'Blockchain Artificial Intelligence Cloud Crypto Software',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_empty_category_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{self.FIXTURE_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': 'Microsoft',
                'model': 'Windows',
                'price': 30000,
                'category': '',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    @parameterized.expand([
        [{
            'model': 'PDP-11',
            'price': 30000,
            'category': 'PC',
        }],
        [{
            'manufacturer': 'IBM',
            'price': 30000,
            'category': 'PC',
        }],
        [{
            'manufacturer': 'IBM',
            'model': 'PDP-11',
            'category': 'PC',
        }],
        [{
            'manufacturer': 'IBM',
            'model': 'PDP-11',
            'price': 30000
        }]
    ])
    def test_update_product_with_missing_attribute_returns_bad_request(self, product_data: dict[str | int]) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{self.FIXTURE_PRODUCT_ID}/',
            json.dumps(product_data),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_product_with_unknown_attribute_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/product/{self.FIXTURE_PRODUCT_ID}/',
            json.dumps({
                'manufacturer': 'IBM',
                'model': 'PDP-11',
                'category': 'PC',
                'price': 999,
                'unknown_field': 'xyz'
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
