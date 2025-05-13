from psycopg2.errors import ForeignKeyViolation

from .db_controller import *
from crud_api.serializers.drivers_serializer import DriversSerializer, driver_convert

logger = logging.getLogger(__name__)


class DriversList:
    def read(self, request):
        logger.info('GET Request for table Drivers')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute('SELECT * FROM Drivers')
                res = driver_convert(cur.fetchall())
                serializer = DriversSerializer(res, many=True)
        except AttributeError as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def create(self, request):
        logger.info('POST Request for table Drivers')
        conn = db_connect()
        data = DriversSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"INSERT INTO Drivers (full_name, phone_number, passport) VALUES ("
                            f"'{data.data['full_name']}', '{data.data['phone_number']}', '{data.data['passport']}') "
                            f"RETURNING *")
                res = cur.fetchall()
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        except psycopg2.errors.UniqueViolation:
            return Response(status=400, data='Invalid data. UNIQUE constraint cannot be satisfied')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=201, data=driver_convert(res))


class DriversDetails:
    def read(self, request, pk):
        logger.info(f'GET Request for table Drivers, row {pk}')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f'SELECT * FROM Drivers WHERE id = {pk}')
                res = driver_convert(cur.fetchall())
                serializer = DriversSerializer(res, many=True)
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def update(self, request, pk):
        logger.info('PUT Request for table Drivers')
        conn = db_connect()
        data = DriversSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"UPDATE Drivers SET full_name = '{data.data['full_name']}', "
                            f"phone_number = '{data.data['phone_number']}', passport = '{data.data['passport']}'"
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
        return Response(status=200, data=driver_convert(res))

    def delete(self, request, pk):
        logger.info('DELETE Request for table Drivers')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"DELETE FROM Drivers WHERE id = {pk}")
        except AttributeError as exc:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=204, data='Content deleted')
