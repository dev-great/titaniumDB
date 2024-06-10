# urls.py
from django.urls import path, include
from .views import ChangePasswordView, DeleteAccount, Logout, RegisterView, LoginView, TokenRefreshView, TokenVerifyView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(),
         name='token_obtain_pair'),

    path('user_profile/', UserProfileView.as_view()),
    path('logout/', Logout.as_view()),
    path('changepassword/', ChangePasswordView.as_view()),
    path('delete_user/', DeleteAccount.as_view()),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('password_reset/', include('django_rest_passwordreset.urls')),
]
