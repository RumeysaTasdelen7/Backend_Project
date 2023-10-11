from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationsViewSet, ReservationCretaeAPIView, ReservationAvailabilityAPIView, ReservationDetailView, ReservationListAllView, ReservationDeleteView, ReservationUpdateView

router = DefaultRouter()
router.register(r'crud', ReservationsViewSet, basename="reservationviewset")

urlpatterns = [
    path("", include(router.urls)),
    path("add/auth", ReservationCretaeAPIView.as_view(), name="car_user_add_reserv"),
    path("add/", ReservationCretaeAPIView.as_view(), name="car_add_reserv"),
    path("auth/", ReservationAvailabilityAPIView.as_view(), name="reserv_availability"),
    path("<int:pk>/auth/", ReservationDetailView.as_view(), name="reserv_detail_auth"),
    path("<int:pk>/admin/", ReservationDetailView.as_view(), name="reserv_detail_admin"),
    path("admin/all", ReservationListAllView.as_view(), name="list_admin_all"),
    path("auth/all", ReservationListAllView.as_view(), name="list_auth"),
    path("admin/auth/all", ReservationListAllView.as_view(), name="list_auth_admin"),
    path("admin/all/pages/", ReservationListAllView.as_view(), name="list_pages_admin"),
    path("admin/<int:pk>/auth", ReservationDeleteView.as_view(), name="reserv_delete"),
    path("admin/auth", ReservationUpdateView.as_view(), name="reserv_update"),
]