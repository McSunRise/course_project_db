from rest_framework import serializers
from dataclasses import dataclass


@dataclass(slots=True)
class CarsDM:
    plate_number: str
    car_name: str
    color: str
    vin: str
    status: str
    id: int = -1


def car_convert(cars: list[tuple]):
    result = []
    for i in cars:
        row = dict(id=i[0], plate_number=i[1], car_name=i[2], color=i[3], vin=i[4], status=i[5])
        result.append(row)
    return result


class CarsSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=-1)
    plate_number = serializers.CharField()
    car_name = serializers.CharField()
    color = serializers.CharField()
    vin = serializers.CharField()
    status = serializers.CharField()

    def to_representation(self, instance):
        instance = CarsDM(**instance)
        return {
            "id": instance.id,
            "plate_number": instance.plate_number,
            "car_name": instance.car_name,
            "color": instance.color,
            "vin": instance.vin,
            "status": instance.status
        }
