from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers

from vendor.models import Vendor


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """Create a user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class VendorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """Create a user with encrypted password along with a Vendor and return it"""
        vendor_name = validated_data.pop('name')
        user = get_user_model().objects.create_user(**validated_data)
        Vendor.objects.create(
            name=vendor_name,
            user=user
        )
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for a user authentication token"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = 'Unable to authenticate user with the given credentials'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user

        return attrs
