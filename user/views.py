from django.http import JsonResponse

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .tasks import send_email_task

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


def send_notification(request):
    subject = "Notification Subject"
    message = "This is a notification message."
    from_email = "your_email@example.com"
    recipient_list = ["recipient@example.com"]

    send_email_task.delay(subject, message, from_email, recipient_list)

    return JsonResponse({"status": "Notification sent"})
