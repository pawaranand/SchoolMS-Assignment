# Generated by Django 2.0.1 on 2018-12-24 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0002_auto_20181224_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examlog',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_question_logs', to='sms.Question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
    ]
