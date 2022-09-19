"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    # 시리얼라이저에 넘겨줄 객체를 정의해준다.
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name'] # 필수로 넘겨줄 파라미터
        extra_kwargs = {'password' : {'write_only' : True, 'min_length' : 5}} # 각각의 필드에 대해 따로 설정해줄 수 있다.

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None) # 한번 패스워드를 꺼내고 삭제한다.
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type' : 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""

        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg =  _('Unable to authenticate with provide credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs