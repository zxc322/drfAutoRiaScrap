from django.db import models


class Car(models.Model):
    title = models.CharField(max_length=200)
    year = models.SmallIntegerField()
    price = models.IntegerField()
    mileage = models.IntegerField(null=True)
    state_number = models.CharField(max_length=30, null=True)
    href = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
