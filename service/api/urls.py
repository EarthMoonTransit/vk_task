from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import Route, SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterView, ChangePasswordView, UserViewSet



router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'friend-requests', FriendRequestViewSet)
router.register(r'friendships', FriendshipViewSet)



urlpatterns = [
    path('users/me/', UserViewSet.as_view(
        {
            'get': 'get_me',
            'patch': 'patch_me',
            'delete': 'delete_me',
        }
    )),
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    #path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
]



'''{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4Mzc5MTE3NywiaWF0IjoxNjgzNzA0Nzc3LCJqdGkiOiJlM2NhNWIwNzBiYTk0MTc3OGYxZjQ4ZGIxNGY4MDNmYiIsInVzZXJfaWQiOjJ9.WQ2Dj7A1NJFF_ObpKhgVtZFTtdceMB03B72Dl8lIRj0",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzODc3NTc3LCJpYXQiOjE2ODM3MDQ3NzcsImp0aSI6Ijg5Mjg5N2Q0YTE3MjQ4YTE4NzU0MDE4YmMzYmJjNjZhIiwidXNlcl9pZCI6Mn0.VuJbf8eZlAoLxAY-_zEH4fv-Y8MZeB2Der3aRXcgoZs"
}'''