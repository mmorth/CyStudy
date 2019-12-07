# Generated by Django 2.0.3 on 2018-03-27 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupchat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('staff_only', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='room',
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='user',
        ),
        migrations.DeleteModel(
            name='ChatMessage',
        ),
        migrations.DeleteModel(
            name='ChatRoom',
        ),
    ]