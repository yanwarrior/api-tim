import http
import json
import jwt

from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from payload_wtf import pwtf

from app.commons.views.bodyparsers import json_parser


class TokenCreateView(View):
    payloader = pwtf.PayloadWTF()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = authenticate(username=body.get('username'),
                                password=body.get('password'))

            if user is not None:
                data = {
                    'username': user.username,
                    'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS)
                }
                token = jwt.encode(data, settings.JWT_SECRET, settings.JWT_ALGORITHM)

                self.payloader.set_state(setter=self.payloader.SET_RESULT, data={
                    'token': token.decode('utf-8'),
                    'bearer': settings.BEARER
                })
                return JsonResponse(self.payloader.todata(), safe=False, status=http.HTTPStatus.OK)

            self.payloader.reset()
            self.payloader.set_state(setter=self.payloader.SET_RESULT, data={'error': 'Wrong credential'})
            return JsonResponse(self.payloader.todata(), safe=False, status=http.HTTPStatus.BAD_REQUEST)

        except Exception as e:
            self.payloader.reset()
            self.payloader.set_state(setter=self.payloader.SET_RESULT, data={'error': str(e)})
            return JsonResponse(self.payloader.todata(), safe=False, status=http.HTTPStatus.BAD_REQUEST)


class TokenVerifyView(View):
    payloader = pwtf.PayloadWTF()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        body = json_parser(request)
        try:
            decoder = jwt.decode(body.get('token'), settings.JWT_SECRET,
                                 algorithms=[settings.JWT_ALGORITHM])
            self.payloader.set_state(setter=self.payloader.SET_RESULT, data=body)
            return JsonResponse(self.payloader.todata(), safe=False, status=http.HTTPStatus.OK)

        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            self.payloader.reset()
            self.payloader.set_state(setter=self.payloader.SET_RESULT, data={'error': 'Token is invalid.'})
            return JsonResponse(self.payloader.todata(), safe=False, status=http.HTTPStatus.BAD_REQUEST)

        except Exception as e:
            self.payloader.reset()
            self.payloader.set_state(setter=self.payloader.SET_RESULT, data={'error': 'Something wrong.'})
            return JsonResponse(self.payloader.todata(), safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)