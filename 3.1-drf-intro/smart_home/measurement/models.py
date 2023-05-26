from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)


class Sensor(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'name: {self.name}' \
               f'description: {self.description}'

    class Meta:

        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        ordering = ['name']


class Measurement(models.Model):

    id_sensore = models.ForeignKey(
        Sensor, on_delete=models.CASCADE
    )
    temperature = models.DecimalField(
        max_digits=4, decimal_places=1
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'id: ' \
               f'temperature: {self.temperature} °C' \
               f'created_at: {self.created_at}'

    class Meta:

        verbose_name = 'Измерение температуры'
        verbose_name_plural = 'Измерение температуры'
        ordering = ['temperature']



