from django.contrib.auth.models import User
from rest_framework import serializers
from user_dashboard.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'bio', 'location', 'date_of_birth']


class DashboardSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        profile = instance.profile
        profile_data = validated_data.pop("profile")
        for key, val in profile_data.items():
            setattr(profile, key, val)
        profile.save()
        user = instance
        for key, val in validated_data.items():
            setattr(user, key, val)
        user.save()
        return user
