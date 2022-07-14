# Generated by Django 4.0 on 2022-07-08 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hls', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servers',
            options={'ordering': ['server_id'], 'verbose_name': '服务器列表', 'verbose_name_plural': '服务器列表'},
        ),
        migrations.RemoveField(
            model_name='servers',
            name='id',
        ),
        migrations.AddField(
            model_name='servers',
            name='front_version',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='前端版本'),
        ),
        migrations.AlterField(
            model_name='servers',
            name='server_id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='游服id'),
        ),
    ]
