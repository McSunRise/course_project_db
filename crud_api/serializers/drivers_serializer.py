from rest_framework import serializers
from dataclasses import dataclass


@dataclass(slots=True)
class DriversDM:
    full_name: str
    phone: str
    passport: str
    rating: float
    id: int = -1


def driver_convert(drivers: list[tuple]):
    result = []
    for i in drivers:
        row = dict(id=i[0], full_name=i[1], phone=i[2], passport=i[3], rating=i[4])
        result.append(row)
    return result


class DriversSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=-1)
    full_name = serializers.CharField()
    phone = serializers.CharField()
    passport = serializers.CharField()
    rating = serializers.FloatField()

    def to_representation(self, instance):
        instance = DriversDM(**instance)
        return {
            "id": instance.id,
            "full_name": instance.full_name,
            "phone": instance.phone,
            "passport": instance.passport,
            "rating": instance.rating
        }
