from psycopg2.errors import ForeignKeyViolation

from .db_controller import *
from crud_api.serializers.cars_serializer import CarsSerializer, car_convert

logger = logging.getLogger(__name__)


class CarsList:
    def read(self, request):
        logger.info('GET Request for table Cars')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute('SELECT * FROM Cars')
                res = car_convert(cur.fetchall())
                serializer = CarsSerializer(res, many=True)
        except AttributeError as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def create(self, request):
        logger.info('POST Request for table Cars')
        conn = db_connect()
        data = CarsSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"INSERT INTO Cars (plate_number, car_name, color, VIN, status) VALUES ("
                            f"'{data.data['plate_number']}', '{data.data['car_name']}', "
                            f"'{data.data['color']}', '{data.data['vin']}', '{data.data['status']}') RETURNING *")
                res = cur.fetchall()
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=201, data=car_convert(res))


class CarsDetails:
    def read(self, request, pk):
        logger.info(f'GET Request for table Cars, row {pk}')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f'SELECT * FROM Cars WHERE id = {pk}')
                res = car_convert(cur.fetchall())
                serializer = CarsSerializer(res, many=True)
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def update(self, request, pk):
        logger.info('PUT Request for table Cars')
        conn = db_connect()
        data = CarsSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"UPDATE Cars SET plate_number = '{data.data['plate_number']}', "
                            f"car_name = '{data.data['car_name']}', color = '{data.data['color']}', "
                            f"vin = '{data.data['vin']}', status = '{data.data['status']}'"
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
        return Response(status=200, data=car_convert(res))

    def delete(self, request, pk):
        logger.info('DELETE Request for table Cars')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"DELETE FROM Cars WHERE id = {pk}")
        except AttributeError as exc:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=204, data='Content deleted')
