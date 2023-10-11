from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from contactmessages.models import Message
from .serializers import MessageSerializer
from rest_framework.response import Response
import math
from core.page_filter import pages_filter


class MessageCreateView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageListView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        if self.request.path == "/contactmessage/request/" or self.request.path == "/contactmessage/request":
            return Message.objects.filter(pk=self.request.query_params.get("id"))
        return Message.objects.all()
    
    def list(self, request,*args, **kwargs):
        if request.path.startswith('/contactmessage/pages/') or request.path.startswith('/contactmessage/pages'):
            return pages_filter(self, request, Message, *args, **kwargs)
        return super().list(request, *args, **kwargs)
    
    
class MessageDetail(RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer