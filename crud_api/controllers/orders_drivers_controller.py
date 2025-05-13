import psycopg2.errors
from psycopg2.errors import ForeignKeyViolation

from .db_controller import *
from crud_api.serializers.orders_drivers_serializer import OrdersDriversSerializer, order_driver_convert

logger = logging.getLogger(__name__)


class OrdersDriversList:
    def read(self, request):
        logger.info('GET Request for table Orders_Drivers')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute('SELECT * FROM Orders_Drivers')
                res = order_driver_convert(cur.fetchall())
                serializer = OrdersDriversSerializer(res, many=True)
        except AttributeError as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def create(self, request):
        logger.info('POST Request for table Orders_Drivers')
        conn = db_connect()
        data = OrdersDriversSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"INSERT INTO Orders_Drivers (order_id, driver_id, car_id) VALUES ("
                            f"{data.data['order_id']}, {data.data['driver_id']}, {data.data['car_id']})"
                            f"RETURNING *")
                res = cur.fetchall()
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        except psycopg2.errors.UniqueViolation:
            return Response(status=400, data='Invalid data. UNIQUE constraint cannot be satisfied')
        except psycopg2.errors.ForeignKeyViolation:
            return Response(status=400, data="Invalid data. FOREIGN KEY doesn't exist")
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=201, data=order_driver_convert(res))


class OrdersDriversDetails:
    def read(self, request, pk):
        logger.info(f'GET Request for table Orders_Drivers, row {pk}')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f'SELECT * FROM Orders_Drivers WHERE order_id = {pk}')
                res = order_driver_convert(cur.fetchall())
                serializer = OrdersDriversSerializer(res, many=True)
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def update(self, request, pk):
        logger.info('PUT Request for table Orders_Drivers')
        conn = db_connect()
        data = OrdersDriversSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"UPDATE Orders_Drivers SET driver_id = {data.data['driver_id']},"
                            f"car_id = {data.data['car_id']} "
                            f"WHERE order_id = {pk} RETURNING *")
                res = cur.fetchall()
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        except ForeignKeyViolation:
            return Response(status=404, data='Invalid data for updating')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=order_driver_convert(res))

    def delete(self, request, pk):
        logger.info('DELETE Request for table Orders_Drivers')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"DELETE FROM Orders_Drivers WHERE order_id = {pk}")
        except AttributeError as exc:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=204, data='Content deleted')
