from .controllers.orders import OrdersList, OrdersDetails
from rest_framework.views import APIView


class OrdersViewsList(APIView):
    def get(self, request):
        return OrdersList().read(request)

    def post(self, request):
        return OrdersList().create(request)


class OrdersViewsDetails(APIView):
    def get(self, request, pk):
        return OrdersDetails().read(request, pk)

    def put(self, request, pk):
        return OrdersDetails().update(request, pk)

    def delete(self, request, pk):
        return OrdersDetails().delete(request, pk)

# Create your views here.
