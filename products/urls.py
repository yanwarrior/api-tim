from django.urls import path
from products import views


app_name = 'products'
urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='categories-detail'),
    path('product-list/', views.product_list, name='product-list'),
    path('product-add/', views.product_add, name='product-add'),
]