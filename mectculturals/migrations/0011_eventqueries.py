# Generated by Django 3.2.7 on 2021-10-25 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mectculturals', '0010_auto_20211025_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventQueries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventid', models.IntegerField(default=0)),
                ('query', models.CharField(max_length=600)),
                ('postedby', models.IntegerField(default=0)),
                ('respondedby', models.IntegerField(default=None)),
                ('response', models.CharField(max_length=600)),
            ],
        ),
    ]
