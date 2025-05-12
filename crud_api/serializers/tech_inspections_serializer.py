from rest_framework import serializers
from datetime import datetime, date
from dataclasses import dataclass


@dataclass(slots=True)
class TechInsDM:
    car_id: int
    mechanic_id: int
    work_type: str
    work_cost: int
    id: int = -1
    inspection_date: date = date.today()


def tech_ins_convert(orders_drivers: list[tuple]):
    result = []
    for i in orders_drivers:
        row = dict(id=i[0], car_id=i[1], mechanic_id=i[2], inspection_date=i[3], work_type=i[4], work_cost=i[5])
        result.append(row)
    return result


class TechInsSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=-1)
    car_id = serializers.IntegerField()
    mechanic_id = serializers.IntegerField()
    inspection_date = serializers.DateField(default=date.today())
    work_type = serializers.CharField()
    work_cost = serializers.IntegerField()

    def to_representation(self, instance):
        instance = TechInsDM(**instance)
        return {
            "id": instance.id,
            "car_id": instance.car_id,
            "mechanic_id": instance.mechanic_id,
            "inspection_date": instance.inspection_date,
            "work_type": instance.work_type,
            "work_cost": instance.work_cost
            }
