# Generated by Django 4.1.5 on 2023-01-29 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.CharField(choices=[('free', 'Свободно'), ('reserved', 'Несвободно')], max_length=50),
        ),
    ]