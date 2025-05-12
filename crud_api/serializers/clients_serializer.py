from rest_framework import serializers
from dataclasses import dataclass


@dataclass(slots=True)
class ClientsDM:
    full_name: str
    rating: float
    phone: str
    email: str
    id: int = -1


def client_convert(clients: list[tuple]):
    result = []
    for i in clients:
        row = dict(id=i[0], full_name=i[1], rating=i[2], phone=i[3], email=i[4])
        result.append(row)
    return result


class ClientsSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=-1)
    full_name = serializers.CharField()
    rating = serializers.FloatField()
    phone = serializers.CharField()
    email = serializers.EmailField()

    def to_representation(self, instance):
        instance = ClientsDM(**instance)
        return {
            "id": instance.id,
            "full_name": instance.full_name,
            "rating": instance.rating,
            "phone": instance.phone,
            "email": instance.email
        }
