from django.shortcuts import get_object_or_404
from rest_framework import filters, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


from .models import User
from .serializers import RegisterSerializer, ChangePasswordSerializer, UserSerializer, FriendRequestSerializer
from .permissions import UserPermission

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    @action(detail=True)
    def get_me(self, request):
        user_data = self.serializer_class(request.user).data
        return Response(user_data)

    @action(detail=True)
    def patch_me(self, request):
        serializer = self.serializer_class(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_me(self, request):
        return Response(status=405)


