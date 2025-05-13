from rest_framework import serializers
from dataclasses import dataclass


@dataclass(slots=True)
class PositionsDM:
    position_name: str
    salary: int
    id: int = -1


def position_convert(orders_drivers: list[tuple]):
    result = []
    for i in orders_drivers:
        row = dict(id=i[0], position_name=i[1], salary=i[2])
        result.append(row)
    return result


class PositionsSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=-1)
    position_name = serializers.CharField()
    salary = serializers.IntegerField()

    def to_representation(self, instance):
        instance = PositionsDM(**instance)
        return {
            "id": instance.id,
            "position_name": instance.position_name,
            "salary": instance.salary
            }
