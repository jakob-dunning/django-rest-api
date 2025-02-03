import json
from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase
from parameterized import parameterized

from api.enums.HttpHeaderContentType import HttpHeaderContentType
from api import models


class CreateUserTestCase(TestCase):

    def test_create_user(self) -> None:
        email: str = 'hansi@haxno.ul'
        name: str = 'Johnny Bravo'

        response: HttpResponse = self.client.post(
            '/api/user/',
            json.dumps({
                'email': email,
                'name': name,
            }),
            content_type=HttpHeaderContentType.JSON
        )
        response_body = json.loads(response.content)

        user = models.User.objects.get(pk=response_body['id'])

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertEqual(user.shopping_cart, None)

    def test_create_user_with_long_email_address_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/user/',
            json.dumps({
                'email': 'karl.friedrich.von.und.zu.boerne@mymotherfuckinglongurl.com',
                'name': 'Karl Friedrich von und zu Börne',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_user_with_empty_email_address_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/user/',
            json.dumps({
                'email': '',
                'name': 'Heinz Strunk',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_user_with_long_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/user/',
            json.dumps({
                'email': 'karl@taxis.com',
                'name': 'Karl-Heinz Eckart von Hirschhausen zu Thurn und Taxis Rothschild',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_user_with_empty_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/user/',
            json.dumps({
                'email': 'hans@nuxt.ll',
                'name': '',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    @parameterized.expand([
        [{
            'email': 'hans@nasa.ff',
        }],
        [{
            'name': 'Hoschi Hans',
        }]
    ])
    def test_create_product_with_missing_attribute_returns_bad_request(self, user_data: dict[str, str]) -> None:
        response: HttpResponse = self.client.post(
            '/api/user/',
            json.dumps(user_data),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_unknown_attribute_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/user/',
            json.dumps({
                'email': 'jksghdf@ffff.dd',
                'name': 'Ozzy XXX',
                'unknown_field': 'xyz'
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
