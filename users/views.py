from rest_framework import viewsets, mixins
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.routers import Route, SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomTokenObtainSerializer


class AnonCreateOnly(BasePermission):
    def has_permissions(self, request, view):
        return (self.request.user.is_authenticated or view.action == 'create')


class UserRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'post': 'create',
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update'
            },
            name='{basename}',
            detail=True,
            initkwargs={'suffix': 'User'}
        ),
    ]


class CRUViewSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):
    pass


class UserAPIViewSet(CRUViewSet):
    permission_classes = (AnonCreateOnly,)
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        return user


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
