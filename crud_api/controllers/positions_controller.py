from psycopg2.errors import ForeignKeyViolation

from .db_controller import *
from crud_api.serializers.positions_serializer import PositionsSerializer, position_convert

logger = logging.getLogger(__name__)


class PositionsList:
    def read(self, request):
        logger.info('GET Request for table Positions')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute('SELECT * FROM Positions')
                res = position_convert(cur.fetchall())
                serializer = PositionsSerializer(res, many=True)
        except AttributeError as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def create(self, request):
        logger.info('POST Request for table Positions')
        conn = db_connect()
        data = PositionsSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"INSERT INTO Positions (position_name, salary) VALUES ("
                            f"'{data.data['position_name']}', {data.data['salary']}) RETURNING *")
                res = cur.fetchall()
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=201, data=position_convert(res))


class PositionsDetails:
    def read(self, request, pk):
        logger.info(f'GET Request for table Positions, row {pk}')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f'SELECT * FROM Positions WHERE id = {pk}')
                res = position_convert(cur.fetchall())
                serializer = PositionsSerializer(res, many=True)
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def update(self, request, pk):
        logger.info('PUT Request for table Positions')
        conn = db_connect()
        data = PositionsSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"UPDATE Positions SET position_name = '{data.data['position_name']}', "
                            f"salary = {data.data['salary']} WHERE id = {pk} RETURNING *")
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
        return Response(status=200, data=position_convert(res))

    def delete(self, request, pk):
        logger.info('DELETE Request for table Positions')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"DELETE FROM Positions WHERE id = {pk}")
        except AttributeError as exc:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=204, data='Content deleted')
