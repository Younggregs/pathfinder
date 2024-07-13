import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Airline(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Airport(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.name


class JourneyPath(BaseModel):
    origin = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="origin_journeys"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="destination_journeys"
    )
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.origin.name} to {self.destination.name} - {self.airline.name}"

    class Meta:
        unique_together = ("origin", "destination", "airline")


class Flight(BaseModel):
    journey_path = models.ForeignKey(JourneyPath, on_delete=models.CASCADE)
    flight_number = models.CharField(max_length=255)
    date = models.DateField()
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    url = models.URLField(max_length=1500)

    def __str__(self):
        return f"{self.journey_path.origin.name} to {self.journey_path.destination.name} - {self.journey_path.airline.name} - {self.date}"


class CachePath(BaseModel):
    origin = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="origin_caches"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="destination_caches"
    )

    def __str__(self):
        return f"{self.origin.name} to {self.destination.name}"

    class Meta:
        unique_together = ("origin", "destination")
