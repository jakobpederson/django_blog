from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import LoginHistory
from .serializers import LoginHistorySerializer, UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token_str = response.data.get("access")
        if response.status_code == status.HTTP_200_OK and token_str:
            if token_str:
                try:
                    token = AccessToken(token_str)
                    user = User.objects.get(id=token["user_id"])
                    LoginHistory.objects.create(
                        user=user,
                        ip_address=self.get_client_ip(request),
                        user_agent=request.META.get("HTTP_USER_AGENT", ""),
                    )
                except Exception as e:
                    raise Exception(
                        f"Error decoding token or creating login history: {e}"
                    )
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LoginHistoryView(generics.ListAPIView):
    serializer_class = LoginHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return LoginHistory.objects.filter(user=self.request.user)
