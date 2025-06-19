from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (CustomTokenObtainPairView, LoginHistoryView, RegisterView,
                    UserProfileView)

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("profile/", UserProfileView.as_view(), name="auth_profile"),
    path("login-history/", LoginHistoryView.as_view(), name="login_history"),
]
