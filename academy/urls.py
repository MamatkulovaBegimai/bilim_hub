from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('courses/<slug:slug>/apply/', views.apply_course, name='apply_course'),

    path('manager/', views.dashboard, name='dashboard'),
    path('manager/applications/', views.application_list, name='application_list'),
    path('manager/applications/<int:pk>/update/', views.application_update, name='application_update'),

    path('manager/groups/', views.group_list, name='group_list'),
    path('manager/groups/create/', views.group_create, name='group_create'),
    path('manager/groups/<int:pk>/', views.group_detail, name='group_detail'),
    path('manager/groups/<int:pk>/edit/', views.group_update, name='group_update'),

    path('manager/students/', views.student_list, name='student_list'),
    path('manager/students/create/', views.student_create, name='student_create'),
    path('manager/students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('manager/students/<int:pk>/remove-from-group/', views.student_remove_from_group, name='student_remove_from_group'),
    path('manager/students/<int:pk>/delete/', views.student_delete, name='student_delete'),
]
