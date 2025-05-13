from psycopg2.errors import ForeignKeyViolation

from .db_controller import *
from crud_api.serializers.assignments_serializer import AssignmentsSerializer, assignments_convert

logger = logging.getLogger(__name__)


class AssignmentsList:
    def read(self, request):
        logger.info('GET Request for table Assignments')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute('SELECT * FROM Assignments')
                res = assignments_convert(cur.fetchall())
                serializer = AssignmentsSerializer(res, many=True)
        except AttributeError as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def create(self, request):
        logger.info('POST Request for table Assignments')
        conn = db_connect()
        data = AssignmentsSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f'INSERT INTO Assignments (driver_id) VALUES ({data.data["driver_id"]})'
                            f"RETURNING *")
                res = cur.fetchall()
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception:
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=201, data=assignments_convert(res))


class AssignmentsDetails:
    def read(self, request, pk):
        logger.info(f'GET Request for table Assignments, row {pk}')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f'SELECT * FROM Assignments WHERE id = {pk}')
                res = assignments_convert(cur.fetchall())
                serializer = AssignmentsSerializer(res, many=True)
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def update(self, request, pk):
        logger.info('PUT Request for table Assignments')
        conn = db_connect()
        data = AssignmentsSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"UPDATE Assignments SET driver_id = {data.data['driver_id']}, "
                            f"assignment_date = '{data.data['assignment_date']}', "
                            f"revenue = {data.data['revenue']} "
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
        return Response(status=200, data=assignments_convert(res))

    def delete(self, request, pk):
        logger.info('DELETE Request for table Assignments')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"DELETE FROM Assignments WHERE id = {pk}")
        except AttributeError as exc:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=204, data='Content deleted')
