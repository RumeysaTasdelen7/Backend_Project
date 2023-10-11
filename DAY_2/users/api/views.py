from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from .serializers import RegisterSerializer, CustomLoginSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters
import math

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
            page = request.query_params.get('page', 1)
            size = request.query_params.get('size', 10)
            sort = request.query_params.get('sort', 'id')
            direction = request.query_params.get('direction', 'asc')

            page = int(page)
            size = int(size)

            if page < 1:
                page=1
            if size < 1:
                size=1

            start_index = (page-1) * size
            end_index = (start_index + size)


            if direction.lower() == 'asc':
                try:
                    users = User.objects.order_by(sort)[start_index:end_index]
                except:
                    users = User.objects.order_by(sort)[start_index]
            
            else:
                try:
                    users = User.objects.order_by(f"-{sort}")[start_index:end_index]
                except:
                    users = User.objects.order_by(f"-{sort}")[start_index]


            serializer = self.serializer_class(users, many=True)
            total_users = User.objects.count()
            total_pages = math.ceil(total_users/size)
            num_elements = len(users)
            data = {
                "totalPages": total_pages,
                "totalElements": total_users,
                "first": start_index+1,
                "last": num_elements,
                "number": num_elements,
                "sort": {
                    "sorted": True,
                    "unsorted": False,
                    "empty": False
                },
                "numberOfElements": num_elements,
                "pagable": {
                    "sort": {
                        "sorted": True,
                        "unsorted": False,
                        "empty": False
                    },
                    "pageNumber": page,
                    "pageSize": size,
                    "paged": True,
                    "unpaged": False,
                    "offset": start_index
                },
                "size": size,
                "content": serializer.data,
                "empty": len(serializer.data) == 0
            }
            return Response(data)
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