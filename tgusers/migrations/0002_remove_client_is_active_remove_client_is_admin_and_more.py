# Generated by Django 5.1.6 on 2025-03-26 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_beat', '0019_alter_periodictasks_options'),
        ('tgusers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='client',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='clienthook',
            name='clientuser',
        ),
        migrations.AddField(
            model_name='client',
            name='clientuser',
            field=models.ManyToManyField(to='tgusers.clienthook'),
        ),
        migrations.AddField(
            model_name='client',
            name='tasks',
            field=models.ManyToManyField(to='django_celery_beat.periodictask'),
        ),
        migrations.AlterField(
            model_name='clienthook',
            name='url',
            field=models.CharField(blank=True, max_length=200, verbose_name='Вебхук'),
        ),
    ]
