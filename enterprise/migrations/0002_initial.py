# Generated by Django 5.0.1 on 2024-06-04 02:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('enterprise', '0001_initial'),
        ('repair', '0001_initial'),
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprise',
            name='repairs',
            field=models.ManyToManyField(blank=True, related_name='enterprise_repairs', to='repair.repair'),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('Staff', 'Staff'), ('Technician', 'Technician')], max_length=10)),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterprise.enterprise')),
            ],
        ),
    ]
