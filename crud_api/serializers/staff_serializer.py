from rest_framework import serializers
from dataclasses import dataclass


@dataclass(slots=True)
class StaffDM:
    position_id: int
    full_name: str
    passport: str
    id: int = -1


def staff_convert(orders_drivers: list[tuple]):
    result = []
    for i in orders_drivers:
        row = dict(id=i[0], position_id=i[1], full_name=i[2], passport=i[3])
        result.append(row)
    return result


class StaffSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=-1)
    position_id = serializers.IntegerField()
    full_name = serializers.CharField()
    passport = serializers.CharField()

    def to_representation(self, instance):
        instance = StaffDM(**instance)
        return {
            "id": instance.id,
            "position_id": instance.position_id,
            "full_name": instance.full_name,
            "passport": instance.passport
            }
