from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


UserModel = get_user_model()


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        return token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'password',)
        extra_kwargs = {
            'username': {'read_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = UserModel.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_extra_kwargs(self):
        extra_kwargs = super(UserSerializer, self).get_extra_kwargs()
        if self.instance is None:
            kwargs = extra_kwargs.get('username', {})
            kwargs['read_only'] = False
            extra_kwargs['username'] = kwargs
        return extra_kwargs
