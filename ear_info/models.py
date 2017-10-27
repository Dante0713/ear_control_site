from django.db import models


# Create your models here.
class Earthquake(models.Model):
    
    ear_id = models.TextField()
    s_year = models.IntegerField()
    s_month = models.IntegerField()
    ear_time = models.TextField()
    ear_longitude = models.FloatField()
    ear_latitude = models.FloatField()
    ear_scale = models.FloatField()
    ear_deep = models.FloatField()
    ear_epicenter_pos = models.TextField()

    class Meta:
        db_table = "ear_info"