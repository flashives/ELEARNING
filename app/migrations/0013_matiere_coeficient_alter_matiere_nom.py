# Generated by Django 5.0.6 on 2024-07-03 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_lesson_description_alter_lesson_niveau_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='matiere',
            name='coeficient',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='matiere',
            name='nom',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
