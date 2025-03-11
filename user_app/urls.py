from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.views import registration_view,logout_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns  = [
    # path('login',obtain_auth_token),
    path('register',registration_view),
    path('logout/',logout_view),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]