from django import forms
from .models import Application
class ApplicationForm(forms.ModelForm):
    class Meta:
        model=Application
        fields=['full_name','phone','email','message']
        widgets={'full_name':forms.TextInput(attrs={'placeholder':'Аты-жөнүңүз'}),'phone':forms.TextInput(attrs={'placeholder':'+996 ...'}),'email':forms.EmailInput(attrs={'placeholder':'name@example.com'}),'message':forms.Textarea(attrs={'rows':4,'placeholder':'Кошумча маалымат (милдеттүү эмес)'})}
