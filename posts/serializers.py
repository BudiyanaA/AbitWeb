from rest_framework import serializers
from .models import Post, Comment, Image
from users.serializers import UserSerializer


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('image',)


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ('comment', 'author', 'created_at')
        extra_kwargs = {'created_at': {'read_only': True}}


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'content', 'category',
                  'images', 'created_at', 'comments', 'updated_at')
        extra_kwargs = {'created_at': {'read_only': True},
                        'updated_at': {'read_only': True}}

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        post = Post.objects.create(**validated_data)
        for image in images_data.values():
            Image.objects.create(post=post, image=image)
        return post
