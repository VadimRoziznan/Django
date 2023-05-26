# Generated by Django 4.2.1 on 2023-05-26 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Sensor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "description",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
            options={
                "verbose_name": "Датчик",
                "verbose_name_plural": "Датчики",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Measurement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("temperature", models.DecimalField(decimal_places=1, max_digits=4)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "id_sensore",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="measurement.sensor",
                    ),
                ),
            ],
            options={
                "verbose_name": "Измерение температуры",
                "verbose_name_plural": "Измерение температуры",
                "ordering": ["temperature"],
            },
        ),
    ]
