import datetime
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
import io
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from users.models import User
from cars.models import Car
from reservations.models import Reservation
from rest_framework.response import Response
import xlsxwriter
import xlwt
# Create your views here.


@api_view(["GET"])
@permission_classes([IsAdminUser])
def export_excel_users(request):
    if request.method == "GET":
        response = HttpResponse(content_type="application/ms-excel")
        response['Content-Disposition']="attachment; filenmae=Users=" + str(datetime.datetime.now()) + ".xls"

        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("Users")
        row_num=0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ["id", "firstNmae", "lastName", "phoneNumber", "address", "zipcode", "builtIn", "roles"]

        for col_num in range(len(columns)):
            ws.write(row_num,col_num,str(columns[col_num]), font_style)

        font_style = xlwt.XFStyle()
        rows = User.objects.all().values_list("id", "firstNmae", "lastName", "phoneNumber", "address", "zipcode", "builtIn", "roles")

        for row in rows:
            row_num+=1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num], font_style))

        wb.save(response)

        return response
    else:
        return HttpResponseNotAllowed(['GET'])
    
@api_view(["GET"])
@permission_classes([IsAdminUser])
def export_user_xlsx(request):
    if request.method=="GET":
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory":True})
        worksheet = workbook.add_worksheet("Users")
        bold = workbook.add_format({"bold": True})

        report = User.objects.all()

        row = 1
        col = 0

        for line in report:
            worksheet.write(row, col, line.id)
            worksheet.write(row, col + 1, line.first_name)
            worksheet.write(row, col + 2, line.last_name)
            worksheet.write(row, col + 3, line.phoneNumber)
            worksheet.write(row, col + 4, line.address)
            worksheet.write(row, col + 5, line.zipCode)
            worksheet.write(row, col + 6, line.builtIn)
            worksheet.write(row, col + 7, line.roles)
            row+=1

        worksheet.write("A1", "id", bold)
        worksheet.write("B1", "first_name", bold)
        worksheet.write("C1", "last_name", bold)
        worksheet.write("D1", "phoneNumber", bold)
        worksheet.write("E1", "address", bold)
        worksheet.write("F1", "zipCode", bold)
        worksheet.write("G1", "builtIn", bold)
        worksheet.write("H1", "roles", bold)
        workbook.close()

        output.seek(0)

        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment, filename=Users.xlsx"

        return response
    
    else:
        return HttpResponseNotAllowed(["GET"])
    


@api_view(["GET"])
@permission_classes([IsAdminUser])
def export_excel_cars(request):

    if request.method == "GET":
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = "attachment; filename=Cars_" + str(datetime.datetime.now()) + ".xls"

        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("Cars")

        row_num=0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ["id", "model", "doors", "seats", "luggage", "transmissio",
                   "airContitioning", "age", "pricePerHour", "fuelType", "builtIn", "image"]
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = Car.objects.all().values_list("id", "model", "doors", "seats", "luggage", "transmissio",
                   "airContitioning", "age", "pricePerHour", "fuelType", "builtIn", "image")
        
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

        wb.save(response)

        return response
    
    else:
        return HttpResponseNotAllowed(["GET"])
    

@api_view(["GET"])
@permission_classes([IsAdminUser])
def export_excel_reservations(request):
    if request.method == "GET":
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = "attachment; filename=Reservations_" + str(datetime.datetime.now()) + ".xls"

        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("Reservations")
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ["id", "pickUpTime", "dropOffTime", "car_id", "user_id", 
                   "pickUpLocation", "dropOffLocation", "status", "totalPrice" ]
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = Reservation.objects.all().values_list("id", "pickUpTime", "dropOffTime", "car_id", "user_id",
                   "pickUpLocation", "dropOffLocation", "status", "totalPrice")
        
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)


        wb.save(response)

        return response
    else:
        return HttpResponseNotAllowed(["GET"])

