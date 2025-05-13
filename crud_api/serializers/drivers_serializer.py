from rest_framework import serializers
from dataclasses import dataclass


@dataclass(slots=True)
class DriversDM:
    full_name: str
    phone_number: str
    passport: str
    rating: float = 2.5
    id: int = -1


def driver_convert(drivers: list[tuple]):
    result = []
    for i in drivers:
        row = dict(id=i[0], full_name=i[1], phone_number=i[2], passport=i[3], rating=i[4])
        result.append(row)
    return result


class DriversSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=-1)
    full_name = serializers.CharField()
    phone_number = serializers.CharField()
    passport = serializers.CharField()
    rating = serializers.FloatField(default=2.5)

    def to_representation(self, instance):
        instance = DriversDM(**instance)
        return {
            "id": instance.id,
            "full_name": instance.full_name,
            "phone_number": instance.phone_number,
            "passport": instance.passport,
            "rating": instance.rating
        }
