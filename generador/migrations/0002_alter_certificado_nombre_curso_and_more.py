# Generated by Django 4.2.15 on 2024-08-20 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generador', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificado',
            name='nombre_curso',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='certificado',
            name='nombre_participante',
            field=models.CharField(max_length=50),
        ),
    ]
