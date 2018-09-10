from django.urls import path
from products import views


app_name = 'products'
urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='categories-detail'),
    path('product-list/', views.product_list, name='product-list'),
    path('product-add/', views.product_add, name='product-add'),
    path('product-detail/<int:pk>/', views.product_detail, name='product-detail'),
    path('product-edit/<int:pk>/', views.product_edit, name='product-edit'),
]