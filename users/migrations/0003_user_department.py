# Generated by Django 4.0 on 2022-07-12 07:32

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=users.models.department_Mode, to='users.department_mode'),
        ),
    ]