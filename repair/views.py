from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import Repair
from rest_framework.response import Response
from .serializers import AdminRepairSerializer,TechnicianRepairSerializer,StaffRepairSerializer
from .permissions import check_status
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils.dateparse import parse_date
# Create your views here.
class RepairView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self,request):
        search = request.GET.get('search')
        user = request.user
        enterprise = user.person.enterprise
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        repairs = Repair.objects.filter(enterprise_repairs__name=enterprise)
        # repairs = Repair.objects.filter(repaired_by__enterprise=enterprise)  # Corrected filtering based on user's enterprise
        print(repairs)
        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            if start_date and end_date:
                repairs = repairs.filter(received_date__range=(start_date, end_date))

        if search:
            if len(search)>40:
                repairs=Repair.objects.none()
            else:
                repair_customer_name= repairs.filter(customer_name__icontains=search)
                repair_phone_model= repairs.filter(phone_model__icontains=search)
                repair_id =repairs.filter(repair_id__exact=search)
                repair_customer_phone_number = repairs.filter(customer_phone_number__icontains=search)
                repairs=  repair_customer_name.union(repair_customer_phone_number,repair_phone_model,repair_id)
            if not repairs:
                return Response("NONE")
        status = check_status(user)

        if status == "Admin":
            serializer = AdminRepairSerializer(repairs,many=True)
        elif status == "Technician":
            serializer = TechnicianRepairSerializer(repairs,many=True)
        else:
            serializer = StaffRepairSerializer(repairs,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        data = request.data
        serializer = AdminRepairSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            enterprise = user.person.enterprise
            obj = serializer.save()     #ALWAYS REMEMBER U FIRST NEED IT TO BE SAVED TO ADD
            enterprise.repairs.add(obj)
            return Response({"msg":"Successful"})
        
    def patch(self,request):
        repair_id = request.data.get('repair_id',None)
        repair = Repair.objects.get(repair_id=repair_id)
        data=request.data
        if repair:
            serializer = AdminRepairSerializer(repair, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"No repair found"})