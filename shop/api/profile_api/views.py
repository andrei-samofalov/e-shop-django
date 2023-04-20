from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from api.profile_api.serializers import AvatarSerializer, ProfileSerializer


class ProfileDetailView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self) -> Profile:
        return Profile.objects.select_related('user').get(
            pk=self.request.user.profile.pk
        )


class PasswordChangeView(APIView):
    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def put(self, request: Request) -> Response:
        obj: User = self.get_object()
        curr_pass = request.data.get('passwordCurrent')
        data = {"errors": "Введен некорректный текущий пароль"}

        if obj.check_password(curr_pass):
            obj.set_password(request.data.get('password'))
            obj.save()
            login(request, obj)
            del data['errors']

        return Response(data)


class AvatarSetView(APIView):
    def get_object(self):
        return Profile.objects.get(pk=self.request.user.profile.pk)

    def post(self, request: Request, *args, **kwargs) -> Response:
        avatar: UploadedFile = request.FILES.get('avatar')
        obj: Profile = self.get_object()

        obj.set_avatar(avatar)
        profile_avatar = AvatarSerializer(obj)

        return Response(profile_avatar.data, status.HTTP_201_CREATED)
