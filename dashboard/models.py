from __future__ import unicode_literals

from django.db import models

class Table1(models.Model):
    locker_id = models.IntegerField(primary_key=True)
    locker_name = models.CharField(db_column='Locker_name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(max_length=45, blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    pincode = models.CharField(max_length=45, blank=True, null=True)
    prime_capacity = models.CharField(max_length=45, blank=True, null=True)
    standard_capacity = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'table1'


class Prime(models.Model):
    key_p = models.AutoField(primary_key=True)
    locker = models.ForeignKey(Table1, on_delete=models.CASCADE)
    day0 = models.IntegerField(blank=True, null=True)
    day1 = models.IntegerField(blank=True, null=True)
    day2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prime'


class Standard(models.Model):
    key_s = models.AutoField(primary_key=True)
    locker = models.ForeignKey(Table1, on_delete=models.CASCADE)
    day0 = models.IntegerField(blank=True, null=True)
    day1 = models.IntegerField(blank=True, null=True)
    day2 = models.IntegerField(blank=True, null=True)
    day3 = models.IntegerField(blank=True, null=True)
    day4 = models.IntegerField(blank=True, null=True)
    day5 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'standard'



