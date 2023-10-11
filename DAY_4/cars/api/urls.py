from django.urls import path
from .views import CarAddView, CarDeleteView, CarDetailView, CarListView, CarUpdateView


urlpatterns = [
    path("admin/<int:imageId>/add/", CarAddView.as_view(), name="car_add"),
    path("visitors/<int:pk>/", CarDetailView.as_view(), name="car_detail"),
    path("visitors/all/", CarListView.as_view(), name="car_all"),
    path("visitors/pages/", CarListView.as_view(), name="car_all_pages"),
    path("admin/<int:pk>/auth/", CarDeleteView.as_view(), name="car_delete"),
    path("admin/auth/", CarUpdateView.as_view(), name="car_update"),
]