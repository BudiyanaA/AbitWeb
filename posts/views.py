from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer
### import generic
from django.views import generic

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS


class IsAdminAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user == obj.author


class PostAPIViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('category',)
    search_fields = ('title', 'content', '=category',)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)


class CommentAPIViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminAuthorOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return Comment.objects.none()
        post_id = self.kwargs['post_id']
        queryset = Comment.objects.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        author = self.request.user
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=author, post=post)

### list post
class PostList(generic.ListView):
    queryset = Post.objects.order_by('-created_at')
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'