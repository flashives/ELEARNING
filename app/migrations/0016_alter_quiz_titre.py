# Generated by Django 5.0.6 on 2024-07-07 00:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_quiz_question_reponse_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='titre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.lesson'),
        ),
    ]
