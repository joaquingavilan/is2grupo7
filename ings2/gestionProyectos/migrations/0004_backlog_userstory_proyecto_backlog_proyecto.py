# Generated by Django 4.1 on 2022-09-12 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionProyectos', '0003_usuario_rol_delete_usuariorol'),
    ]

    operations = [
        migrations.CreateModel(
            name='Backlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('backlog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionProyectos.backlog')),
                ('usuarios', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionProyectos.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('usuarios', models.ManyToManyField(to='gestionProyectos.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='backlog',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionProyectos.proyecto'),
        ),
    ]