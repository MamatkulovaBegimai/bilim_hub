from django.db import models
from django.utils import timezone


class Course(models.Model):
    title=models.CharField('Курстун аталышы',max_length=180)
    slug=models.SlugField(unique=True)
    short_description=models.CharField('Кыскача маалымат',max_length=280)
    description=models.TextField('Толук маалымат',blank=True)
    duration=models.CharField('Узактыгы',max_length=80,blank=True)
    price=models.DecimalField('Баасы',max_digits=10,decimal_places=2,default=0)
    is_active=models.BooleanField('Активдүү',default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['title']; verbose_name='Курс'; verbose_name_plural='Курстар'
    def __str__(self): return self.title
    
    
class Application(models.Model):
    class Status(models.TextChoices):
        NEW='new','Жаңы'; CONTACTED='contacted','Байланыш түзүлдү'; ACCEPTED='accepted','Кабыл алынды'; REJECTED='rejected','Четке кагылды'
    course=models.ForeignKey(Course,on_delete=models.PROTECT,related_name='applications',verbose_name='Курс')
    full_name=models.CharField('Аты-жөнү',max_length=180)
    phone=models.CharField('Телефон',max_length=30)
    email=models.EmailField('Электрондук почта',blank=True)
    message=models.TextField('Кошумча маалымат',blank=True)
    status=models.CharField('Статусу',max_length=20,choices=Status.choices,default=Status.NEW)
    created_at=models.DateTimeField('Түшкөн убактысы',default=timezone.now)
    manager_note=models.TextField('Менеджердин эскертүүсү',blank=True)
    student=models.OneToOneField('Student',on_delete=models.SET_NULL,null=True,blank=True,related_name='source_application',verbose_name='Түзүлгөн студент')
    class Meta: ordering=['-created_at']; verbose_name='Окууга арыз'; verbose_name_plural='Окууга арыздар'
    def __str__(self): return f'{self.full_name} — {self.course}'
    
    
class StudyGroup(models.Model):
    name=models.CharField('Топтун аталышы',max_length=120)
    course=models.ForeignKey(Course,on_delete=models.PROTECT,related_name='groups',verbose_name='Курс')
    start_date=models.DateField('Башталган күнү',null=True,blank=True)
    end_date=models.DateField('Аяктаган күнү',null=True,blank=True)
    is_active=models.BooleanField('Активдүү',default=True)
    class Meta: ordering=['name']; verbose_name='Окуу тобу'; verbose_name_plural='Окуу топтору'
    def __str__(self): return self.name
    
    
class Student(models.Model):
    full_name=models.CharField('Аты-жөнү',max_length=180)
    phone=models.CharField('Телефон',max_length=30)
    email=models.EmailField('Электрондук почта',blank=True)
    study_group=models.ForeignKey(StudyGroup,on_delete=models.SET_NULL,null=True,blank=True,related_name='students',verbose_name='Окуу тобу')
    enrolled_at=models.DateField('Катталган күнү',default=timezone.localdate)
    is_active=models.BooleanField('Окуп жатат',default=True)
    class Meta: ordering=['full_name']; verbose_name='Студент'; verbose_name_plural='Студенттер'
    def __str__(self): return self.full_name
