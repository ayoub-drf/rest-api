# Generated by Django 5.1.2 on 2024-11-15 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_1', '0003_alter_apikey_api_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='api_key',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]