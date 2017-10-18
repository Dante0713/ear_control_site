from django.db import models


# Create your models here.
class Earthquake(models.Model):

    s_year = models.IntegerField()
    s_month = models.IntegerField()
    ear_id = models.TextField()
    ear_time = models.TextField()
    ear_longitude = models.TextField()
    ear_latitude = models.TextField()
    ear_scale = models.TextField()
    ear_deep = models.TextField()
    ear_epicenter_pos = models.TextField()

    class Meta:
        db_table = "ear_info"