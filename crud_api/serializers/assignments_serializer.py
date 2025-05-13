from rest_framework import serializers
from datetime import date
from dataclasses import dataclass


@dataclass(slots=True)
class AssignmentsDM:
    driver_id: int
    revenue: int = 0
    id: int = -1
    assignment_date: date = date.today()


def assignments_convert(orders_drivers: list[tuple]):
    result = []
    for i in orders_drivers:
        row = dict(id=i[0], driver_id=i[1], assignment_date=i[2], revenue=i[3])
        result.append(row)
    return result


class AssignmentsSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=-1)
    driver_id = serializers.IntegerField()
    assignment_date = serializers.DateField(default=date.today())
    revenue = serializers.IntegerField(default=0)

    def to_representation(self, instance):
        instance = AssignmentsDM(**instance)
        return {
            "id": instance.id,
            "driver_id": instance.driver_id,
            "assignment_date": instance.assignment_date,
            "revenue": instance.revenue
            }
