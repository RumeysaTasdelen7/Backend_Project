from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationsViewSet, ReservationCretaeAPIView

router = DefaultRouter()
router.register(r'crud', ReservationsViewSet, basename="reservationviewset")

urlpatterns = [
    path("", include(router.urls)),
    path("add/auth", ReservationCretaeAPIView.as_view(), name="car_user_add_reserv"),
    path("add/", ReservationCretaeAPIView.as_view(), name="car_add_reserv"),
]