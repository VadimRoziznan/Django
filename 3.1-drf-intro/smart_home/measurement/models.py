from django.db import models


class Sensor(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'name: {self.name}, ' \
               f'description: {self.description}'

    class Meta:

        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        ordering = ['name']


class Measurement(models.Model):

    id_sensor = models.ForeignKey(
        Sensor, on_delete=models.CASCADE, related_name='measurements'
    )
    temperature = models.DecimalField(
        max_digits=4, decimal_places=1
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'id датчика: {self.id_sensor}' \
               f'temperature: {self.temperature} °C' \
               f'created_at: {self.created_at}'

    class Meta:

        verbose_name = 'Измерение температуры'
        verbose_name_plural = 'Измерение температуры'
        ordering = ['temperature']
