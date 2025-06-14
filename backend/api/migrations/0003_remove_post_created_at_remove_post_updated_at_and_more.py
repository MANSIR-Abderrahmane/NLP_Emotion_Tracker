# Generated by Django 5.2.1 on 2025-05-25 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_post_options_rename_timestamp_post_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='post',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='post',
            name='true_emotion_label',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.CharField(default='anonymous', max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='emotion_primary',
            field=models.CharField(default='neutral', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='emotion_score',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='external_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='secondary_emotions_json',
            field=models.JSONField(default=dict),
        ),
    ]
