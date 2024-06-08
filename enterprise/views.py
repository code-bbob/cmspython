from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from repair.models import Repair
from repair.permissions import check_status
from django.utils.dateparse import parse_date
from datetime import datetime, date
from .serializers import AdminProfitSerializer,TechnicianProfitSerializer

class EnterpriseProfit(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        enterprise = user.person.enterprise
        repairs = Repair.objects.filter(enterprise_repairs__name=enterprise,repair_status="Completed")
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        status = check_status(user)

       
        # If start_date or end_date is not provided, use the start of the current month
        if not start_date or not end_date:
            today = date.today()
            start_date = today.replace(day=1)  # First day of the current month
            end_date = today

        # Parse the dates
        start_date = parse_date(start_date) if isinstance(start_date, str) else start_date
        end_date = parse_date(end_date) if isinstance(end_date, str) else end_date

        # Filter repairs by the date range
        if start_date and end_date:
            repairs = repairs.filter(received_date__range=(start_date, end_date))

        # Return the profits based on user status
        if status == "Admin":
             # Initialize total profits
            total_profit = 0
            technician_profit = 0
            my_profit = 0

            for repair in repairs:
                total_profit += repair.repair_profit
                technician_profit += repair.technician_profit
                my_profit += repair.my_profit
            profit = AdminProfitSerializer(repairs,many=True)

            return Response({"total_profit": total_profit, "technician_profit": technician_profit, "my_profit": my_profit,"data":profit.data})
        

        elif status == "Technician":
            user=user.id
            total_profit = 0
            technician_profit = 0
            repairs = repairs.filter(repaired_by=user)
            for repair in repairs:
                total_profit += repair.repair_profit
                technician_profit += repair.technician_profit
            profit = TechnicianProfitSerializer(repairs,many=True)

            return Response({"total_profit": total_profit, "technician_profit": technician_profit,"data":profit.data})
        
        else:
            return Response({"message": "No profit data available for your role"}, status=status.HTTP_400_BAD_REQUEST)
