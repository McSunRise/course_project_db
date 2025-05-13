from rest_framework import serializers
from dataclasses import dataclass


@dataclass(slots=True)
class OrdersDriversDM:
    order_id: int
    driver_id: int
    car_id: int
    order_price: int = 0


def order_driver_convert(orders_drivers: list[tuple]):
    result = []
    for i in orders_drivers:
        row = dict(order_id=i[0], driver_id=i[1], car_id=i[2], order_price=i[3])
        result.append(row)
    return result


class OrdersDriversSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    driver_id = serializers.IntegerField()
    car_id = serializers.IntegerField()
    order_price = serializers.IntegerField(default=0)

    def to_representation(self, instance):
        instance = OrdersDriversDM(**instance)
        return {
            "order_id": instance.order_id,
            "driver_id": instance.driver_id,
            "car_id": instance.car_id,
            "order_price": instance.order_price
            }
