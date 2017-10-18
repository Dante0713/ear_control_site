from django.conf import settings
from rest_framework import serializers
from ear_info.models import Earthquake


class EarthquakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Earthquake
        fields = ('id', 's_year', 's_month', 'ear_id', 'ear_time', 'ear_longitude', 'ear_latitude', 'ear_scale', 'ear_deep', 'ear_epicenter_pos')

