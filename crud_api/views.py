from .controllers import orders_controller, assignments_controller, cars_controller, drivers_controller, \
    orders_drivers_controller, clients_controller, positions_controller, staff_controller, tech_inspection_controller
from rest_framework.views import APIView


class OrdersViewsList(APIView):
    def get(self, request):
        return orders_controller.OrdersList().read(request)

    def post(self, request):
        return orders_controller.OrdersList().create(request)


class OrdersViewsDetails(APIView):
    def get(self, request, pk):
        return orders_controller.OrdersDetails().read(request, pk)

    def put(self, request, pk):
        return orders_controller.OrdersDetails().update(request, pk)

    def delete(self, request, pk):
        return orders_controller.OrdersDetails().delete(request, pk)


class AssignmentsViewsList(APIView):
    def get(self, request):
        return assignments_controller.AssignmentsList().read(request)

    def post(self, request):
        return assignments_controller.AssignmentsList().create(request)


class AssignmentsViewsDetails(APIView):
    def get(self, request, pk):
        return assignments_controller.AssignmentsDetails().read(request, pk)

    def put(self, request, pk):
        return assignments_controller.AssignmentsDetails().update(request, pk)

    def delete(self, request, pk):
        return assignments_controller.AssignmentsDetails().delete(request, pk)


class CarsViewsList(APIView):
    def get(self, request):
        return cars_controller.CarsList().read(request)

    def post(self, request):
        return cars_controller.CarsList().create(request)


class CarsViewsDetails(APIView):
    def get(self, request, pk):
        return cars_controller.CarsDetails().read(request, pk)

    def put(self, request, pk):
        return cars_controller.CarsDetails().update(request, pk)

    def delete(self, request, pk):
        return cars_controller.CarsDetails().delete(request, pk)


class DriversViewsList(APIView):
    def get(self, request):
        return drivers_controller.DriversList().read(request)

    def post(self, request):
        return drivers_controller.DriversList().create(request)


class DriversViewsDetails(APIView):
    def get(self, request, pk):
        return drivers_controller.DriversDetails().read(request, pk)

    def put(self, request, pk):
        return drivers_controller.DriversDetails().update(request, pk)

    def delete(self, request, pk):
        return drivers_controller.DriversDetails().delete(request, pk)


class OrdersDriversViewsList(APIView):
    def get(self, request):
        return orders_drivers_controller.OrdersDriversList().read(request)

    def post(self, request):
        return orders_drivers_controller.OrdersDriversList().create(request)


class OrdersDriversViewsDetails(APIView):
    def get(self, request, pk):
        return orders_drivers_controller.OrdersDriversDetails().read(request, pk)

    def put(self, request, pk):
        return orders_drivers_controller.OrdersDriversDetails().update(request, pk)

    def delete(self, request, pk):
        return orders_drivers_controller.OrdersDriversDetails().delete(request, pk)


class ClientsViewsList(APIView):
    def get(self, request):
        return clients_controller.ClientsList().read(request)

    def post(self, request):
        return clients_controller.ClientsList().create(request)


class ClientsViewsDetails(APIView):
    def get(self, request, pk):
        return clients_controller.ClientsDetails().read(request, pk)

    def put(self, request, pk):
        return clients_controller.ClientsDetails().update(request, pk)

    def delete(self, request, pk):
        return clients_controller.ClientsDetails().delete(request, pk)


class PositionsViewsList(APIView):
    def get(self, request):
        return positions_controller.PositionsList().read(request)

    def post(self, request):
        return positions_controller.PositionsList().create(request)


class PositionsViewsDetails(APIView):
    def get(self, request, pk):
        return positions_controller.PositionsDetails().read(request, pk)

    def put(self, request, pk):
        return positions_controller.PositionsDetails().update(request, pk)

    def delete(self, request, pk):
        return positions_controller.PositionsDetails().delete(request, pk)


class StaffViewsList(APIView):
    def get(self, request):
        return staff_controller.StaffList().read(request)

    def post(self, request):
        return staff_controller.StaffList().create(request)


class StaffViewsDetails(APIView):
    def get(self, request, pk):
        return staff_controller.StaffDetails().read(request, pk)

    def put(self, request, pk):
        return staff_controller.StaffDetails().update(request, pk)

    def delete(self, request, pk):
        return staff_controller.StaffDetails().delete(request, pk)


class TechInsViewsList(APIView):
    def get(self, request):
        return tech_inspection_controller.TechInsList().read(request)

    def post(self, request):
        return tech_inspection_controller.TechInsList().create(request)


class TechInsViewsDetails(APIView):
    def get(self, request, pk):
        return tech_inspection_controller.TechInsDetails().read(request, pk)

    def put(self, request, pk):
        return tech_inspection_controller.TechInsDetails().update(request, pk)

    def delete(self, request, pk):
        return tech_inspection_controller.TechInsDetails().delete(request, pk)

# Create your views here.
