import http
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from payload_wtf import pwtf

from app.commons.decorators import auth_with_token
from app.commons.views import paginators
from app.commons.views.bodyparsers import json_parser
from products.facade_filter import FacadeCategoryFilter
from products.models import Category


class CategoryListView(View):

    model = Category
    payload = pwtf.PayloadWTF()
    paging = paginators
    facade = FacadeCategoryFilter

    @method_decorator(csrf_exempt)
    @method_decorator(auth_with_token)
    def dispatch(self, *args, **kwargs):
        return super(CategoryListView, self).dispatch(*args, **kwargs)

    def get_queryset(self, request):
        categories = self.model.objects.all()
        facade = self.facade(categories)
        facade.filter_by_id(request.GET.get('id', ''))
        facade.filter_by_name(request.GET.get('name', ''))

        return facade.get_result()

    def get(self, request):
        categories = self.get_queryset(request)
        categories, self.payload = self.paging.paginate(request, categories, self.payload, 1)

        data = []
        for category in categories:
            data.append({
                'id': category.id,
                'name': category.name
            })

        self.payload.set_state(setter=self.payload.SET_RESULT, data=data)
        return JsonResponse(self.payload.todata(), safe=False, status=http.HTTPStatus.OK)

    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        Category.objects.create(name=body.get('name'))
        self.payload.reset()
        self.payload.set_state(setter=self.payload.SET_RESULT, data={'message': 'Success create data'})

        return JsonResponse(self.payload.todata(), safe=False, status=http.HTTPStatus.CREATED)


class CategoryDetailView(View):
    model = Category
    payload = pwtf.PayloadWTF()

    @method_decorator(csrf_exempt)
    @method_decorator(auth_with_token)
    def dispatch(self, *args, **kwargs):
        return super(CategoryDetailView, self).dispatch(*args, **kwargs)

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, pk):
        category = self.get_object(pk)
        self.payload.set_state(setter=self.payload.SET_RESULT, data={
            'id': category.id,
            'name': category.name
        })

        return JsonResponse(self.payload.todata(), safe=False, status=http.HTTPStatus.OK)

    def put(self, request, pk):
        body = json_parser(request)

        category = self.get_object(pk)
        category.name = body.get('name')
        category.save()

        self.payload.reset()
        self.payload.set_state(setter=self.payload.SET_RESULT, data={'message': 'Success update category'})

        return JsonResponse(self.payload.todata(), safe=False, status=http.HTTPStatus.OK)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()

        self.payload.reset()
        self.payload.set_state(setter=self.payload.SET_RESULT, data={'message': 'Success delete category'})

        return JsonResponse(self.payload.todata(), safe=False, status=http.HTTPStatus.NO_CONTENT)


