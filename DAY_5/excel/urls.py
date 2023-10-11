from django.urls import path
from .views import export_excel_cars, export_excel_reservations, export_excel_users, export_user_xlsx


urlpatterns = [
    path("download/users/", export_excel_users, name="users-excel"),
    # path("download/users/", export_user_xlsx, name="users-excel"),
    path("download/cars/", export_excel_cars, name="cars-excel"),
    path("download/reservations/", export_excel_reservations, name="reservations-excel"),
]