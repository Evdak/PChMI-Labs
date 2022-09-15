from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('laba1/', include("laba1.urls")),
]
