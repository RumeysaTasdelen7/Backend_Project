from django.urls import path
from .views import MessageCreateView, MessageListView, MessageDetail

urlpatterns = [
    path("visitors/", MessageCreateView.as_view(), name="create_message"),
    path("", MessageListView.as_view(), name="list_all_messages"),
    path("request/", MessageListView.as_view(), name="list_request_message"),
    path("pages/", MessageListView.as_view(), name="message_list_pages"),
    path("<int:pk>/", MessageDetail.as_view(), name="message_detail"),
]