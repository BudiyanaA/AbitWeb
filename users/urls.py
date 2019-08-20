from django.urls import path, include
from .views import UserRouter, UserAPIViewSet, CustomTokenObtainView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)


router = UserRouter()
router.register('', UserAPIViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainView.as_view(), name='token_obtain'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
]
