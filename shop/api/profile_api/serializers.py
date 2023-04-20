from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        optional_fields = ('avatar',)
        fields = (
            'fullName',
            'email',
            'phone',
            'avatar',
        )

    fullName = serializers.CharField(read_only=False)
    email = serializers.EmailField(read_only=False)


class PasswordChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('url',)

    url = serializers.SerializerMethodField('get_avatar_url')

    @classmethod
    def get_avatar_url(cls, obj: Profile):
        return obj.avatar.url
