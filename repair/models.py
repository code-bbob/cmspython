from django.db import models
from datetime import datetime
import random
import string
# from django.conf import settings

# Create your models here.


class Repair(models.Model):

    status_choices = [
        ("Not repaired", "Not repaired"),
        ("Repaired","Repaired"),
        ("Unrepairable","Unrepairable"),
        ("Outrepaired", "Outrepaired"),
        ("Completed","Completed")
    ]

    accessory_choices = [
        ("Present","Present"),
        ("Absent","Absent"),
    ]

    # company = models.CharField(max_length=30)
    repair_id = models.CharField(max_length=8,blank=True)
    customer_name = models.CharField(max_length=30)
    customer_phone_number = models.CharField(max_length=10)
    phone_model = models.CharField(max_length=30)   
    repair_problem = models.CharField(max_length=50)
    repair_description = models.TextField(null=True, blank=True)
    imei_number = models.CharField(max_length=30,null=True, blank=True)
    model_number = models.CharField(max_length=30,null=True, blank=True)
    sim_tray =models.CharField(max_length=20,choices=accessory_choices,default="Present")
    sim = models.CharField(max_length=20,choices=accessory_choices,default="Absent")
    SD_card = models.CharField(max_length=20,choices=accessory_choices,default="Absent")
    phone_cover = models.CharField(max_length=20,choices=accessory_choices,default="Absent")
    phone_condition = models.CharField(max_length=30,null=True, blank=True)
    total_amount = models.IntegerField()
    advance_paid = models.IntegerField()
    due = models.IntegerField()
    received_date = models.DateField(default=datetime.now)
    received_by = models.CharField(max_length=30)
    repaired_by = models.ForeignKey('enterprise.Person', limit_choices_to={'role': 'Technician'}, null=True, blank=True, on_delete=models.SET_NULL)
    outside_repair = models.BooleanField(default=False)
    delivery_date = models.DateField(default=datetime.now)
    repair_status=models.CharField(max_length=20,choices=status_choices,default="Not repaired")
    amount_paid = models.FloatField(null=True,blank=True)
    repair_cost_price = models.FloatField(null=True,blank=True)
    cost_price_description = models.CharField(max_length=50,null=True,blank=True)
    repair_profit = models.FloatField(null=True,blank=True)
    technician_profit = models.FloatField(null=True,blank=True)
    my_profit = models.FloatField(null=True, blank=True)
    outside_name = models.CharField(max_length=30,null=True,blank=True)
    outside_desc = models.CharField(max_length=30,null=True,blank=True)
    taken_by = models.CharField(max_length=30,null=True,blank=True)
    outside_cost = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is new
            self.repair_id = self.generate_unique_repair_id()
        if self.repair_status=="Completed":
            self.amount_paid = self.amount_paid + self.advance_paid
        if self.repair_status=="Completed" and self.amount_paid is not None and self.repair_cost_price is not None:
            self.repair_profit = self.amount_paid - self.repair_cost_price
            if self.outside_repair:
                self.my_profit = self.repair_profit
                self.technician_profit = 0
            else:
                
                enterprises = self.enterprise_repairs.all()
                if not enterprises:
                    self.technician_profit = 0
                    self.my_profit = self.repair_profit  # Or any other default value
                else:
                    enterprise = enterprises.first()  # Get the first related enterprise, adjust as needed
                    self.technician_profit = (enterprise.technician_profit / 100) * self.repair_profit
                    self.my_profit = ((100 - enterprise.technician_profit) / 100) * self.repair_profit
                # self.technician_profit = (self.enterprise.technician_profit / 100) * self.repair_profit
                # self.my_profit = ((100-self.enterprise.technician_profit) / 100) * self.repair_profit
        super(Repair, self).save(*args, **kwargs)

    def generate_unique_repair_id(self,length=8):
        characters = string.ascii_letters + string.digits
        while True:
            repair_id = ''.join(random.choice(characters) for _ in range(length))
            if not Repair.objects.filter(repair_id=repair_id).exists():
                return repair_id
            
    def __str__(self):
        return f"{self.phone_model} by {self.customer_name}"
    

