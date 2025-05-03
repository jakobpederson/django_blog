from django.shortcuts import render
from rest_framework import generics, permissions

from user_dashboard.serializers import DashboardSerializer
from user_dashboard.models import UserProfile


class DashboardView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DashboardSerializer

    def get_object(self):
        return self.request.user
