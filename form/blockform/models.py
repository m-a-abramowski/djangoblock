from django.db import models



class Address(models.Model):
    address = models.CharField(max_length=100)
    n_tx = models.IntegerField()
    total_received = models.BigIntegerField()
    total_sent = models.BigIntegerField()
    final_balance = models.BigIntegerField()

class Transaction(models.Model):
    tx_id = models.CharField(max_length=100)
    size = models.IntegerField()
    weight = models.IntegerField()
    output = models.BigIntegerField(default = 0,null=True, blank=True)
    negativeoutput = models.BigIntegerField(default = 0,null=True, blank=True)
    time = models.DateTimeField()
    addressRel = models.ForeignKey(Address, on_delete=models.CASCADE)

# Create your models here.
