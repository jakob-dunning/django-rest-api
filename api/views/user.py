import json
from http import HTTPStatus
from typing import Final

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import models


@method_decorator(csrf_exempt, name='dispatch')
class User(View):
    MUTABLE_USER_ATTRIBUTES: Final[set[str]] = {'email', 'name'}

    def get(self, _, user_id: int) -> JsonResponse:
        try:
            user: models.User = models.User.objects.get(pk=user_id)
            return JsonResponse(model_to_dict(user))
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'User with id: {user_id} not found'}, status=HTTPStatus.NOT_FOUND)

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            post_data: dict[str, str | int] = json.loads(request.body)

            differing_keys: set[str] = self._get_diff_of_input_keys_and_mutable_user_keys(post_data)
            if len(differing_keys) > 0:
                return JsonResponse({'error': f'Missing or wrong attribute(s) for model user: {differing_keys}'},
                                    status=HTTPStatus.BAD_REQUEST)

            user: models.User = models.User(
                email=post_data.get('email'),
                name=post_data.get('name'),
                shopping_cart=None
            )
            user.clean_fields()
            user.save()
            return JsonResponse(model_to_dict(user))
        except ValidationError as validation_error:
            return JsonResponse(validation_error.message_dict, status=HTTPStatus.BAD_REQUEST)

    def put(self, request: HttpRequest, user_id: int) -> JsonResponse:
        try:
            put_data: dict[str, str | int] = json.loads(request.body)
            user: models.User = models.User.objects.get(pk=user_id)

            differing_keys: set[str] = self._get_diff_of_input_keys_and_mutable_user_keys(put_data)
            if len(differing_keys) > 0:
                return JsonResponse({'error': f'Missing or wrong attribute(s) for model user: {differing_keys}'},
                                    status=HTTPStatus.BAD_REQUEST)

            for key, value in put_data.items():
                setattr(user, key, value)
            user.clean_fields()
            user.save()
            return JsonResponse(model_to_dict(user))
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'User with id: {user_id} not found'}, status=HTTPStatus.NOT_FOUND)
        except ValidationError as validation_error:
            return JsonResponse(validation_error.message_dict, status=HTTPStatus.BAD_REQUEST)

    def delete(self, _, user_id: int) -> JsonResponse:
        try:
            models.User.objects.get(pk=user_id).delete()
            return JsonResponse({}, status=HTTPStatus.NO_CONTENT)
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'User with id: {user_id} not found'}, status=HTTPStatus.NOT_FOUND)

    def _get_diff_of_input_keys_and_mutable_user_keys(self, input_data: dict[str, str | int]) -> set[str]:
        return self.MUTABLE_USER_ATTRIBUTES.symmetric_difference(set(input_data.keys()))
