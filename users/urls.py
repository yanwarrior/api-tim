from django.urls import path
from users import views


app_name = 'users'
urlpatterns = [
    path('token-create/', views.TokenCreateView.as_view(), name='token-create'),
]