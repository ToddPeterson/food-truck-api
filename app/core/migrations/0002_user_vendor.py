# Generated by Django 3.0.8 on 2020-07-09 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='vendor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendor.Vendor'),
        ),
    ]