from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ApplicationForm
from .models import Application, Course, Student, StudyGroup
def home(request): return render(request,'academy/home.html',{'courses':Course.objects.filter(is_active=True)[:6]})
def course_list(request): return render(request,'academy/course_list.html',{'courses':Course.objects.filter(is_active=True)})
def course_detail(request,slug): return render(request,'academy/course_detail.html',{'course':get_object_or_404(Course,slug=slug,is_active=True)})
def apply_course(request,slug):
    course=get_object_or_404(Course,slug=slug,is_active=True)
    if request.method=='POST':
        form=ApplicationForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False); obj.course=course; obj.save(); messages.success(request,'Арызыңыз кабыл алынды. Менеджер сиз менен байланышат.'); return redirect('course_detail',slug=course.slug)
    else: form=ApplicationForm()
    return render(request,'academy/application_form.html',{'form':form,'course':course})
@staff_member_required
def dashboard(request):
    return render(request,'academy/dashboard.html',{'new_applications':Application.objects.filter(status='new').count(),'applications_count':Application.objects.count(),'students_count':Student.objects.count(),'groups_count':StudyGroup.objects.count(),'recent_applications':Application.objects.select_related('course')[:8]})
@staff_member_required
def application_list(request):
    qs=Application.objects.select_related('course'); status=request.GET.get('status',''); query=request.GET.get('q','').strip()
    if status: qs=qs.filter(status=status)
    if query: qs=qs.filter(Q(full_name__icontains=query)|Q(phone__icontains=query)|Q(course__title__icontains=query))
    return render(request,'academy/application_list.html',{'applications':qs,'status':status,'q':query,'status_choices':Application.Status.choices})
@staff_member_required
def application_update(request,pk):
    obj=get_object_or_404(Application,pk=pk)
    if request.method=='POST':
        status=request.POST.get('status',obj.status)
        if status in Application.Status.values: obj.status=status
        obj.manager_note=request.POST.get('manager_note',''); obj.save(update_fields=['status','manager_note']); messages.success(request,'Арыз жаңыртылды.')
    return redirect('application_list')
