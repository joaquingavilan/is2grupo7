# Generated by Django 4.1 on 2022-09-07 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionProyectos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rol',
            name='id_permiso',
        ),
        migrations.AddField(
            model_name='rol',
            name='permisos',
            field=models.ManyToManyField(to='gestionProyectos.permiso'),
        ),
    ]
