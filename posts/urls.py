from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostAPIViewSet, CommentAPIViewSet
### import views for template
from . import views

router = DefaultRouter()
router.register('', PostAPIViewSet)
router.register(r'(?P<post_id>[0-9]+)/comments', CommentAPIViewSet, base_name='comment')

urlpatterns = [
    path('api/', include(router.urls)),
    ### interface post list
    path('', views.PostList.as_view(),name='home'),
    path('<created_at>/', views.PostDetail.as_view(), name='post_detail'),
]
