"""ear_control_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from ear_info import views

router = DefaultRouter()
router.register(r'earthquake', views.EarthquakeViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^ear_data/$', views.get_earthquake_data,name='get_earthquake_data'),
    url(r'^ear_chart/$', views.get_chart_data,name='get_chart_data'),
    url(r'^earthquakes/$', views.EarthquakeList),
    url(r'^ear_widgets/$', views.WidgeList),
    url(r'^ear_map/$', views.ShowMap),
]