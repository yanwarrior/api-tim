from django.urls import path
from products import views


app_name = 'products'
urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='categories'),
]