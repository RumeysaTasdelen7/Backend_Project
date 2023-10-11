import mimetypes
import os
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from imagess.models import Image
from .serializers import ImageSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, Http404
from core import settings


class UploadFileView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        file_serializer = ImageSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response({
                "message": "Image upload success",
                "success": True,
                "imageId": str(file_serializer.data["id"])
            }, status=201)
        else:
            return Response(file_serializer.errors, status=400)
        

class ListAllFilesView(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


def download_file(request, image_id):
    try:
        file=Image.objects.get(id=image_id)
    except:
        raise Http404
    
    file_path=os.path.join(settings.MEDIA_ROOT, str(file.image))
    if not os.path.exists(file_path):
        raise Http404
    
    with open(file_path, "rb") as file_content:
        response = HttpResponse(file_content.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = "attachment; filename="+os.path.basename(file_path)

        return response
    

def display_image(request, image_id):
    file = get_object_or_404(Image, id=image_id)

    file_path = os.path.join(settings.MEDIA_ROOT, str(file.image))

    if not os.path.exists(file_path):
        raise Http404

    created, file_ext = os.path.splitext(file_path)

    content_type, create = mimetypes.guess_type(file_ext)

    with open(file_path, "rb") as file_content:
        response = HttpResponse(file_content, content_type="image/jpeg")
        return response
    

@api_view(['DELETE'])
def delete_file(request, image_id):
    file = get_object_or_404(Image, id=image_id)

    file_path = os.path.join(settings.MEDIA_ROOT, str(file.image))

    if not os.path.exists(file_path):
        raise Http404
    
    os.remove(file_path)
    file.delete()

    response = Response({"message": "File and instance deleted successfully"})
    return response