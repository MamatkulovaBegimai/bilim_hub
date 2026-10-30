from django import forms
from .models import Application, Student, StudyGroup


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['full_name', 'phone', 'email', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Аты-жөнүңүз'}),
            'phone': forms.TextInput(attrs={'placeholder': '+996 ...'}),
            'email': forms.EmailInput(attrs={'placeholder': 'name@example.com'}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Кошумча маалымат (милдеттүү эмес)'}),
        }


class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['name', 'course', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', 'Аяктоо күнү башталган күндөн эрте болбошу керек.')
        return cleaned_data


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'phone', 'email', 'study_group', 'enrolled_at', 'is_active']
        widgets = {
            'enrolled_at': forms.DateInput(attrs={'type': 'date'}),
            'study_group': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'study_group': 'Окуу тобу',
        }
