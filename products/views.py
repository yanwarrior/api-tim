from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.commons.decorators import auth_with_token


class CategoryListView(View):

    @method_decorator(csrf_exempt)
    @method_decorator(auth_with_token)
    def dispatch(self, *args, **kwargs):
        return super(CategoryListView, self).dispatch(*args, **kwargs)

    def get(self, request):
        return JsonResponse({'ok': request.user.username})

    def post(self):
        pass
