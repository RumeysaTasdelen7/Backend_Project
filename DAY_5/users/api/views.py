from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from .serializers import RegisterSerializer, CustomLoginSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters
import math
from core.page_filter import pages_filter

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Registration successfully done', 'success': True})
    

class LoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        access_token = str(AccessToken.for_user(user))

        return Response({"token": access_token})
    

class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["firstName", "email"]


    def get_queryset(self):
        queryset = User.objects.all()

        if self.request.path == '/user/':
            return User.objects.filter(id=self.request.user.id)
        else:
            return queryset
        
    def list(self, request, *args, **kwargs):
        if request.path.startswith('/user/auth/pages/') or request.path.startswith('/user/auth/pages'):
            return pages_filter(self, request, User, *args, **kwargs)
        return super().list(request, *args, **kwargs)
    

class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs)
        return Response({"update": "successful", "success": True})    