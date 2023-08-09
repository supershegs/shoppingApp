from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,TokenVerifyView
)
from .views import *


urlpatterns = [
    path('test/', test.as_view()),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserAuthenticationView.as_view(), name='user-login'),
    path('check/', CustomerView.as_view(), name='check'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('profile/', profile.as_view(), name='profile'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('categories/<int:category_id>/', CategoryView.as_view(), name='category-detail'),
    path('products/', ProductView.as_view(), name='products'),
    path('products/<int:product_id>/', ProductView.as_view(), name='product-detail'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('orders/<int:order_id>/', OrderView.as_view(), name='orders-detail'),
    path('carts/', CartView.as_view(), name='carts'),
    path('carts/<int:cart_id>/', CartView.as_view(), name='carts-detail'),
]
