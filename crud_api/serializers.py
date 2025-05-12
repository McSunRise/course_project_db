from rest_framework import serializers
from datetime import datetime
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class OrdersDM:
    client_id: int
    starting_address: str
    finish_address: str
    price: int
    status: str
    id: int = -1
    order_datetime: datetime = datetime.now()


def order_convert(orders: list[tuple]):
    result = []
    for i in orders:
        row = dict(id=i[0], client_id=i[1], order_datetime=i[2], starting_address=i[3], finish_address=i[4],
                   price=i[5], status=i[6])
        result.append(row)
    return result


class OrdersSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=-1)
    client_id = serializers.IntegerField()
    order_datetime = serializers.DateTimeField(default=datetime.now())
    starting_address = serializers.CharField()
    finish_address = serializers.CharField()
    price = serializers.IntegerField()
    status = serializers.CharField()

    def to_representation(self, instance):
        instance = OrdersDM(**instance)
        return {
            "id": instance.id,
            "client_id": instance.client_id,
            "order_datetime": instance.order_datetime,
            "starting_address": instance.starting_address,
            "finish_address": instance.finish_address,
            "price": instance.price,
            "status": instance.status
        }
