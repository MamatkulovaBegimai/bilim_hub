from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ApplicationForm, StudentForm, StudyGroupForm
from .models import Application, Course, Student, StudyGroup


def home(request):
    return render(request, 'academy/home.html', {'courses': Course.objects.filter(is_active=True)[:6]})


def course_list(request):
    return render(request, 'academy/course_list.html', {'courses': Course.objects.filter(is_active=True)})


def course_detail(request, slug):
    return render(request, 'academy/course_detail.html', {'course': get_object_or_404(Course, slug=slug, is_active=True)})


def apply_course(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.save()
            messages.success(request, 'Арызыңыз кабыл алынды. Менеджер сиз менен байланышат.')
            return redirect('course_detail', slug=course.slug)
    else:
        form = ApplicationForm()
    return render(request, 'academy/application_form.html', {'form': form, 'course': course})


@staff_member_required
def dashboard(request):
    context = {
        'new_applications': Application.objects.filter(status='new').count(),
        'applications_count': Application.objects.count(),
        'students_count': Student.objects.count(),
        'groups_count': StudyGroup.objects.count(),
        'recent_applications': Application.objects.select_related('course')[:8],
        'active_groups': StudyGroup.objects.filter(is_active=True).select_related('course').order_by('name')[:5],
    }
    return render(request, 'academy/dashboard.html', context)


@staff_member_required
def application_list(request):
    qs = Application.objects.select_related('course')
    status = request.GET.get('status', '')
    query = request.GET.get('q', '').strip()
    if status in Application.Status.values:
        qs = qs.filter(status=status)
    if query:
        qs = qs.filter(
            Q(full_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(course__title__icontains=query)
        )
    return render(request, 'academy/application_list.html', {
        'applications': qs,
        'status': status,
        'q': query,
        'status_choices': Application.Status.choices,
    })


@staff_member_required
@require_POST
def application_update(request, pk):
    obj = get_object_or_404(Application, pk=pk)
    status = request.POST.get('status', obj.status)
    if status in Application.Status.values:
        obj.status = status
    obj.manager_note = request.POST.get('manager_note', '').strip()
    obj.save(update_fields=['status', 'manager_note'])
    messages.success(request, 'Арыз жаңыртылды.')
    return redirect('application_list')


@staff_member_required
def group_list(request):
    groups = StudyGroup.objects.select_related('course').prefetch_related('students')
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    if query:
        groups = groups.filter(Q(name__icontains=query) | Q(course__title__icontains=query))
    if status == 'active':
        groups = groups.filter(is_active=True)
    elif status == 'inactive':
        groups = groups.filter(is_active=False)
    return render(request, 'academy/group_list.html', {
        'groups': groups,
        'q': query,
        'status': status,
    })


@staff_member_required
def group_create(request):
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f'«{group.name}» тобу түзүлдү.')
            return redirect('group_detail', pk=group.pk)
    else:
        form = StudyGroupForm()
    return render(request, 'academy/group_form.html', {'form': form, 'page_title': 'Жаңы топ түзүү'})


@staff_member_required
def group_update(request, pk):
    group = get_object_or_404(StudyGroup, pk=pk)
    if request.method == 'POST':
        form = StudyGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Топтун маалыматы жаңыртылды.')
            return redirect('group_detail', pk=group.pk)
    else:
        form = StudyGroupForm(instance=group)
    return render(request, 'academy/group_form.html', {
        'form': form,
        'group': group,
        'page_title': 'Топту өзгөртүү',
    })


@staff_member_required
def group_detail(request, pk):
    group = get_object_or_404(StudyGroup.objects.select_related('course'), pk=pk)
    students = group.students.all()
    return render(request, 'academy/group_detail.html', {
        'group': group,
        'students': students,
        'students_count': students.count(),
    })


@staff_member_required
def student_list(request):
    students = Student.objects.select_related('study_group', 'study_group__course')
    query = request.GET.get('q', '').strip()
    group_id = request.GET.get('group', '')
    if query:
        students = students.filter(
            Q(full_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        )
    if group_id == 'none':
        students = students.filter(study_group__isnull=True)
    elif group_id.isdigit():
        students = students.filter(study_group_id=int(group_id))
    return render(request, 'academy/student_list.html', {
        'students': students,
        'groups': StudyGroup.objects.order_by('name'),
        'q': query,
        'selected_group': group_id,
    })


@staff_member_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'«{student.full_name}» студент катары кошулду.')
            if student.study_group_id:
                return redirect('group_detail', pk=student.study_group_id)
            return redirect('student_list')
    else:
        initial = {}
        group_id = request.GET.get('group')
        if group_id and group_id.isdigit():
            initial['study_group'] = get_object_or_404(StudyGroup, pk=int(group_id)).pk
        form = StudentForm(initial=initial)
    return render(request, 'academy/student_form.html', {'form': form, 'page_title': 'Жаңы студент кошуу'})


@staff_member_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Студенттин маалыматы жаңыртылды.')
            if student.study_group_id:
                return redirect('group_detail', pk=student.study_group_id)
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'academy/student_form.html', {
        'form': form,
        'student': student,
        'page_title': 'Студенттин маалыматын өзгөртүү',
    })


@staff_member_required
@require_POST
def student_remove_from_group(request, pk):
    student = get_object_or_404(Student, pk=pk)
    group_id = student.study_group_id
    student.study_group = None
    student.save(update_fields=['study_group'])
    messages.success(request, f'«{student.full_name}» студент группага бекитүүдөн чыгарылды.')
    if group_id:
        return redirect('group_detail', pk=group_id)
    return redirect('student_list')


@staff_member_required
@require_POST
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student_name = student.full_name
    student.delete()
    messages.success(request, f'«{student_name}» студент өчүрүлдү.')
    return redirect('student_list')
