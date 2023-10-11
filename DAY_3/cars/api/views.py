from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from ..models import Car
from .serializers import CarSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

import math

class CarAddView(CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "Car created successfully", "success": True})
    

class CarDetailView(RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CarListView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def list(self, request, *args, **kwargs):
        if request.path.startswith('/car/visitors/pages/') or request.path.startswith('/car/visitors/pages'):
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
                    Cars = Car.objects.order_by(sort)[start_index:end_index]
                except:
                    Cars = Car.objects.order_by(sort)[start_index]
            
            else:
                try:
                    Cars = Car.objects.order_by(f"-{sort}")[start_index:end_index]
                except:
                    Cars = Car.objects.order_by(f"-{sort}")[start_index]


            serializer = self.serializer_class(Cars, many=True, context={"request": request}, *args, **kwargs)
            total_cars = Car.objects.count()
            total_pages = math.ceil(total_cars/size)
            num_elements = len(Cars)
            data = {
                "totalPages": total_pages,
                "totalElements": total_cars,
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
    

class CarDeleteView(DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Car deleted successfully", "success": True})
    
# class CarUpdateView(APIView):
#     def put(self, request, *args, **kwargs):
#         car_id = request.query_params.get('id')
#         image_id = request.query_params.get('imageId')
        
#         try:
#             car=Car.objects.get(id=car_id)
#         except Car.DoesNotExist:
#             return Response({'detail': 'Car not found.'},status=404)
        
#         serializer= CarSerializer(car, data=request.data)
#         if serializer.is_valid():
#             serializer.save(image=image_id)
#             return Response({"message":"Car updated successfully", "success":True})
#         return Response(serializer.errors, status=400)

class CarUpdateView(UpdateAPIView):
    queryset = Car.objects.all() # güncellenecek nesnelerin sorgusu için kullanılır
    serializer_class = CarSerializer # nesnelerin seri hale getirilmesi için kullanılır

    def update(self, request, *args, **kwargs): # HTTP PUT isteği geldiğinde çağrılır ve nesneyi güncellemek için gereken işlemleri gerçekleştirir
        partial = kwargs.pop('partial', False) #partial adında bir değişken, kwargs'dan çıkarılır ve varsayılan olarak False olarak ayarlanır. Bu, kısmi güncellemeleri işlemek için kullanılır.
        car_id = request.query_params.get('pk')
        image_id = request.query_params.get('imageId')
# query_params aracılığıyla car_id ve image_id'yi alırız. 
# Bu, isteği gönderenin URL'de belirttiği parametrelerdir
        if car_id is None:
            return Response({"detail": "Car ID is missing in the request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"detail": "Car not found"}, status=status.HTTP_404_NOT_FOUND)
# Car modelini kullanarak car_id'ye göre ilgili aracı almaya çalışırız. 
# Eğer araç bulunamazsa Car.DoesNotExist istisnasıyla bir 404 hata yanıtı döner.
        
        # Gelen verileri temizle
        cleaned_data = {key: value for key, value in request.data.items() if value is not None}
        
        serializer = self.get_serializer(instance=car, data=cleaned_data, partial=partial)
# self.get_serializer yöntemini kullanarak gelen verileri kullanarak bir 
# seri oluştururuz. Bu seri, CarSerializer tarafından tanımlanan kurallara 
# göre doldurulur. Eğer partial True ise, kısmi güncelleme yapılır.


        if serializer.is_valid():
            # image_id boşsa veya None ise, image'i temizle
            if not image_id:
                serializer.validated_data['image'] = []

            serializer.save()
            return Response({"message": "Car updated successfully", "success": True})
# Seri doğru bir şekilde oluşturulursa ve geçerliyse, veriyi kaydederiz 
# ve bir başarılı yanıt döneriz.       

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Seri geçerli değilse, hataları içeren bir yanıt döneriz.