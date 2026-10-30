from django.contrib import admin
from .models import Application,Course,Student,StudyGroup
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=('title','price','duration','is_active'); list_filter=('is_active',); search_fields=('title','short_description'); prepopulated_fields={'slug':('title',)}
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display=('full_name','course','phone','status','created_at'); list_filter=('status','course','created_at'); search_fields=('full_name','phone','email'); readonly_fields=('created_at',)
@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin): list_display=('name','course','start_date','is_active'); list_filter=('course','is_active')
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin): list_display=('full_name','phone','study_group','is_active'); list_filter=('is_active','study_group'); search_fields=('full_name','phone','email')
