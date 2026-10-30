# Generated for linking an accepted application to one student.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('academy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='student',
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='source_application',
                to='academy.student',
                verbose_name='Түзүлгөн студент',
            ),
        ),
    ]
