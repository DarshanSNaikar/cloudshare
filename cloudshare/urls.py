from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path('admin/', admin.site.urls),

    # connect mediaapp urls
    path('', include('mediaapp.urls')),

]