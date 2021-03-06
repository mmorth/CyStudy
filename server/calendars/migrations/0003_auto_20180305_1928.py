# Generated by Django 2.0.2 on 2018-03-06 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0002_auto_20180212_0845'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(default=None)),
                ('day', models.IntegerField(default=None)),
                ('year', models.IntegerField(default=None)),
                ('location', models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='event', to='calendars.Event')),
            ],
        ),
        migrations.DeleteModel(
            name='Calendar',
        ),
        migrations.AddField(
            model_name='meeting',
            name='month',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='meeting',
            name='year',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='day',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='location',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
