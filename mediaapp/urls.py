from django.urls import path
from . import views

urlpatterns = [

    # authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # dashboard
    path('', views.home, name='home'),
path('dashboard/', views.dashboard, name='dashboard'),

    # upload
    path('upload/', views.upload, name='upload'),

    # generate share link
    path('generate-link/<int:id>/', views.generate_link, name='generate_link'),

    # delete media
    path('delete/<int:id>/', views.delete_media, name='delete_media'),

    # share page
    path('share/<str:code>/', views.view_share, name='share'),

]