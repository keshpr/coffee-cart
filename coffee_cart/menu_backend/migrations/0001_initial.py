# Generated by Django 2.2 on 2019-04-21 08:43

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('ingredients', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Snack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drinks', models.ManyToManyField(to='menu_backend.Drink')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='menu_backend.Item')),
            ],
        ),
        migrations.AddField(
            model_name='drink',
            name='item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='menu_backend.Item'),
        ),
    ]
