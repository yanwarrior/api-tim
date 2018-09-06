import http
import functools
import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from payload_wtf import pwtf


def auth_with_token(f):
    payload = pwtf.PayloadWTF()

    @functools.wraps(f)
    def wrap(request, *args, **kwargs):
        try:
            bearer, token = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')

            if not token:
                payload.set_state(setter=payload.SET_RESULT, data={'error': 'Authorization needed.'})
                return JsonResponse(payload.todata(), safe=False, status=http.HTTPStatus.BAD_REQUEST)

            if not bearer:
                payload.set_state(setter=payload.SET_RESULT, data={'error': 'Bearer needed.'})
                return JsonResponse(payload.todata(), safe=False, status=http.HTTPStatus.BAD_REQUEST)

            data_jwt = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            request.user = User.objects.get(username=data_jwt['username'])
            return f(request, *args, **kwargs)

        except jwt.DecodeError as e:
            payload.reset()
            payload.set_state(setter=payload.SET_RESULT, data={'error': 'Token is invalid.'})
            return JsonResponse(payload.todata(), safe=False, status=http.HTTPStatus.BAD_REQUEST)

        except jwt.ExpiredSignatureError as e:
            payload.reset()
            payload.set_state(setter=payload.SET_RESULT, data={'error': 'Token expired.'})
            return JsonResponse(payload.todata(), safe=False, status=http.HTTPStatus.BAD_REQUEST)

        except Exception as e:
            payload.reset()
            payload.set_state(setter=payload.SET_RESULT, data={'error': str(e)})
            return JsonResponse(payload.todata(), safe=False, status=http.HTTPStatus.BAD_REQUEST)

    return wrap