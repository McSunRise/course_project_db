from psycopg2.errors import ForeignKeyViolation

from .db_controller import *
from crud_api.serializers.orders_serializer import OrdersSerializer, order_convert

logger = logging.getLogger(__name__)


class OrdersList:
    def read(self, request):
        logger.info('GET Request for table Orders')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute('SELECT * FROM Orders')
                res = order_convert(cur.fetchall())
                serializer = OrdersSerializer(res, many=True)
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(serializer.data)

    def create(self, request):
        logger.info('POST Request for table Orders')
        conn = db_connect()
        data = OrdersSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f'INSERT INTO Orders (client_id, starting_address, finish_address, price, status) VALUES '
                            f"({data.data['client_id']}, '{data.data['starting_address']}', "
                            f"'{data.data['finish_address']}', {data.data['price']}, '{data.data['status']}')"
                            f"RETURNING *")
                res = cur.fetchall()
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception:
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=201, data=order_convert(res))


class OrdersDetails:
    def read(self, request, pk):
        logger.info(f'GET Request for table Orders, row {pk}')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f'SELECT * FROM Orders WHERE id = {pk}')
                res = order_convert(cur.fetchall())
                serializer = OrdersSerializer(res, many=True)
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(serializer.data)

    def update(self, request, pk):
        logger.info('PUT Request for table Orders')
        conn = db_connect()
        data = OrdersSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"UPDATE Orders SET client_id = {data.data['client_id']}, "
                            f"order_datetime = '{data.data['order_datetime']}', "
                            f"starting_address = '{data.data['starting_address']}', "
                            f"finish_address = '{data.data['finish_address']}', "
                            f"price = {data.data['price']}, status = '{data.data['status']}' "
                            f"WHERE id = {pk} RETURNING *")
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
        return Response(status=200, data=order_convert(res))

    def delete(self, request, pk):
        logger.info('DELETE Request for table Orders')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"DELETE FROM Orders WHERE id = {pk}")
        except AttributeError as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Connection with database was NOT established')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=204)

# Create your views here.
