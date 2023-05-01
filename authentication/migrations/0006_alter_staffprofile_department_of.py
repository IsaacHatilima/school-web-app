# Generated by Django 4.1.4 on 2023-05-01 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0003_department_members_alter_department_created_by'),
        ('authentication', '0005_staffprofile_department_of'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffprofile',
            name='department_of',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='administration.department'),
        ),
    ]
