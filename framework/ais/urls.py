from django.urls import path
from . import views  # Impor views untuk digunakan dalam routing

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about', views.about, name='about'),  # Sesuaikan dengan string URL
    path('student/', views.student_index, name='student_index'), #Read
    path('student/create/', views.student_create, name='student_create'),# Create
]

