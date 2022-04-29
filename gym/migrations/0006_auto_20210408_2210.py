# Generated by Django 3.1.2 on 2021-04-08 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0005_auto_20210408_2013'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('contact', models.CharField(max_length=10)),
                ('emailid', models.CharField(max_length=50)),
                ('age', models.CharField(max_length=10)),
                ('gender', models.CharField(max_length=10)),
                ('joindate', models.CharField(max_length=40)),
                ('salary', models.CharField(max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Trainer',
        ),
    ]
