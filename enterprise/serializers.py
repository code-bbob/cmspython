from .models import Enterprise
from rest_framework import serializers
from repair.models import Repair
  
class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = '__all__'

class AdminProfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = ['repair_profit','technician_profit','my_profit','repaired_by']

class TechnicianProfitSerializer(serializers.ModelSerializer):
    repaired_by= serializers.SerializerMethodField()
    class Meta:
        model = Repair
        fields = ['repair_profit','technician_profit','repaired_by']
    
    def get_repaired_by(self,obj):
        return obj.repaired_by.user.name