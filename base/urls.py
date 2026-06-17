from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('admin/', views.adminDashboard, name='admin-dashboard'),
    path('teacher/', views.teacherDashboard, name='teacher-dashboard'),
    path('student/', views.studentDashboard, name='student-dashboard'),
    path('approve-teacher/<str:pk>/', views.approveTeacher, name='approve-teacher'),

]

