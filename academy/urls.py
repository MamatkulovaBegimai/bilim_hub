from django.urls import path
from . import views
urlpatterns=[path('',views.home,name='home'),path('courses/',views.course_list,name='course_list'),path('courses/<slug:slug>/',views.course_detail,name='course_detail'),path('courses/<slug:slug>/apply/',views.apply_course,name='apply_course'),path('manager/',views.dashboard,name='dashboard'),path('manager/applications/',views.application_list,name='application_list'),path('manager/applications/<int:pk>/update/',views.application_update,name='application_update')]
