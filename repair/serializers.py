from rest_framework import serializers
from .models import Repair



class AdminRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = '__all__'

class TechnicianRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = '__all__'
class StaffRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = ['repair_id','customer_name']

