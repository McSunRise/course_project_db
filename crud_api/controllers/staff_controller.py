from psycopg2.errors import ForeignKeyViolation

from .db_controller import *
from crud_api.serializers.staff_serializer import StaffSerializer, staff_convert

logger = logging.getLogger(__name__)


class StaffList:
    def read(self, request):
        logger.info('GET Request for table Staff')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute('SELECT * FROM Staff')
                res = staff_convert(cur.fetchall())
                serializer = StaffSerializer(res, many=True)
        except AttributeError as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def create(self, request):
        logger.info('POST Request for table Staff')
        conn = db_connect()
        data = StaffSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"INSERT INTO Staff (position_id, full_name, passport) VALUES ("
                            f"{data.data['position_id']}, '{data.data['full_name']}', '{data.data['passport']}') "
                            f"RETURNING *")
                res = cur.fetchall()
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        except psycopg2.errors.ForeignKeyViolation:
            return Response(status=400, data='Invalid data. Couldn\'t meet FOREIGN KEY requirement')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=201, data=staff_convert(res))


class StaffDetails:
    def read(self, request, pk):
        logger.info(f'GET Request for table Staff, row {pk}')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f'SELECT * FROM Staff WHERE id = {pk}')
                res = staff_convert(cur.fetchall())
                serializer = StaffSerializer(res, many=True)
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def update(self, request, pk):
        logger.info('PUT Request for table Staff')
        conn = db_connect()
        data = StaffSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"UPDATE Staff SET position_id = {data.data['position_id']}, "
                            f"full_name = '{data.data['full_name']}', passport = '{data.data['passport']}' WHERE id = {pk} RETURNING *")
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
        return Response(status=200, data=staff_convert(res))

    def delete(self, request, pk):
        logger.info('DELETE Request for table Staff')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"DELETE FROM Staff WHERE id = {pk}")
        except AttributeError as exc:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=204, data='Content deleted')
