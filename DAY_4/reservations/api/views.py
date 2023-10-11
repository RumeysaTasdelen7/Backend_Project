from rest_framework.viewsets import ModelViewSet
from ..models import Reservation
from .serializers import ReservationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView


class ReservationsViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ReservationCretaeAPIView(CreateAPIView):
    serializer_class = ReservationSerializer
    def post (self, request, formal=None):
        user_id = None
        if request.path == '/reservations/add/auth' or request.path == '/reservations/add/auth':
            user_id = request.query_params.get("userId")
        elif request.user.is_authenticated:
            user_id = request.user.id
        car_id = request.query_params.get("carId")

        if not user_id or not car_id:
            return Response(
                {
                    "error":"userId and carId are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = request.data.copy()

        data["user_id"] = user_id
        data['car_id'] = car_id

        serializer = ReservationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'message':"Reservations created succesfully", "success": True
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    