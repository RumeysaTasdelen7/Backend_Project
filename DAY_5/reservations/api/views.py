from rest_framework.viewsets import ModelViewSet
from ..models import Reservation
from .serializers import ReservationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.exceptions import NotFound, PermissionDenied
from core.page_filter import pages_filter

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
    

class ReservationAvailabilityAPIView(APIView):
    def get(self, request, format=None):
        car_id = request.query_params.get('carId')
        pick_up_date_time = request.query_params.get('pickUpDateTime')
        drop_off_date_time = request.query_params.get('dropOffTime')

        if not car_id or not pick_up_date_time or not drop_off_date_time:
            return Response(
                {
                    "error": "carId, pickUpDateTime and dropOffTime are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservations = Reservation.objects.filter(
            car_id = car_id,
            dropOffTime__gte=pick_up_date_time,
            pickUpDateTime__lte=drop_off_date_time
        )

        if reservations.exists():
            return Response(
                {
                    "message": "Car is not availeble for this time period"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {
                    "message": "Car is availeble for this time period",
                    "success": True
                },
                status=status.HTTP_200_OK
            )
        
class ReservationDetailView(RetrieveAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        pk=self.kwargs["pk"]
        queryset=Reservation.objects.none()
        if not pk:
            raise NotFound("There is no id in the url")
        
        if self.request.path.endswith("/auth/"):
            user_id = self.request.user.id
            if not user_id:
                raise PermissionDenied("User is not authenticated")
            queryset = Reservation.objects.filter(user_id)
            if not queryset:
                raise NotFound("This user does not have any rezervations in this id")
            return queryset
        
        if self.request.path.endswith("/admin/"):
            if self.request.user.is_staff:
                queryset = Reservation.objects.all()
            else:
                raise NotFound("This user is not admin")
            return queryset
        
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                raise NotFound("There is no rezervation")
            return super().get(request, *args, **kwargs)
        except(NotFound, PermissionDenied) as e:
            return Response(str(e), status=e.status_code)
        
class ReservationListAllView(ListAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):

        if self.request.path == "/reservations/admin/all" and self.request.user.is_staff:
            return Reservation.objects.all()
        elif self.request.path == "/reservations/admin/all" and not self.request.user.is_staff:
            return Reservation.objects.none()
        
        if self.request.user.is_staff:
            return Reservation.objects.all()
        elif self.request.user.is_authenticated:
            return Reservation.objects.filter(user_id=self.request.user.id)
        else:
            return Reservation.objects.none()
        
    
    def list(self, request, *args, **kwargs):
        if request.path == "/reservations/auth/all":
            return pages_filter(self, request, Reservation, *args, **kwargs)
        elif request.path == "/reservations/admin/auth/all/":
            return pages_filter(self, request, Reservation, *args, **kwargs)
        elif request.path == "/reservations/admin/all/pages/":
            return pages_filter(self, request, Reservation, *args, **kwargs)
        
        return super().list(request, *args, **kwargs)
    
class ReservationDeleteView(DestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def destroy(self, request, *args, **kwargs):
        if request.user.is_staff:
            pk=self.kwargs["pk"]
            super().destroy(request, *args, **kwargs)
            return Response(
                {
                    "message": f"Reservation-{pk} is deleted succesfully",
                    "success": True
                }
            )
        return Response({
            "message":"Only Admin can deleted reservations"
        },status=status.HTTP_401_UNAUTHORIZED
        )
    
class ReservationUpdateView(UpdateAPIView):
    serializer_class = ReservationSerializer

    def put(self, request, *args, **kwargs):
        reserv_id = request.query_params.get("reservationId")
        car_id = request.query_params.get("carId")
        self.kwargs["pk"] = reserv_id
        if not reserv_id or not car_id:
            return Response(
                {
                    "error": "id and carId are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.user.is_staff:
            data = request.data.copy()

            data["id"] = reserv_id
            data["car_id"] = car_id
            instance = Reservation.objects.filter(id=reserv_id).first()
            serializer = ReservationSerializer(instance, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Reservation updated succesfully",
                        "success": True
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        "message":"Only Admin can updated reservations"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )