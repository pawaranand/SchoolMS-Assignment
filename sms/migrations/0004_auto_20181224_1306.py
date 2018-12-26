# Generated by Django 2.0.1 on 2018-12-24 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0003_auto_20181224_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='examresult',
            name='evaluated',
            field=models.FloatField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='examlog',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_question_logs', to='sms.Exam'),
        ),
        migrations.AlterField(
            model_name='examresult',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_results', to='sms.Exam'),
        ),
        migrations.AlterField(
            model_name='examresult',
            name='score',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='examresult',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_results', to='sms.Student'),
        ),
        migrations.AlterField(
            model_name='studentcourse',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_courses', to='sms.Student'),
        ),
    ]