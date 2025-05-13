from psycopg2.errors import ForeignKeyViolation

from .db_controller import *
from crud_api.serializers.clients_serializer import ClientsSerializer, client_convert

logger = logging.getLogger(__name__)


class ClientsList:
    def read(self, request):
        logger.info('GET Request for table Clients')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute('SELECT * FROM Clients')
                res = client_convert(cur.fetchall())
                serializer = ClientsSerializer(res, many=True)
        except AttributeError as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def create(self, request):
        logger.info('POST Request for table Clients')
        conn = db_connect()
        data = ClientsSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"INSERT INTO Clients (full_name, rating, phone, email) VALUES ("
                            f"'{data.data['full_name']}', {data.data['rating']}, '{data.data['phone']}', "
                            f"'{data.data['email']}') RETURNING *")
                res = cur.fetchall()
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=201, data=client_convert(res))


class ClientsDetails:
    def read(self, request, pk):
        logger.info(f'GET Request for table Clients, row {pk}')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f'SELECT * FROM Clients WHERE id = {pk}')
                res = client_convert(cur.fetchall())
                serializer = ClientsSerializer(res, many=True)
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def update(self, request, pk):
        logger.info('PUT Request for table Clients')
        conn = db_connect()
        data = ClientsSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"UPDATE Clients SET full_name = '{data.data['full_name']}', "
                            f"rating = '{data.data['rating']}', phone = '{data.data['phone']}', "
                            f"email = '{data.data['email']}' WHERE id = {pk} RETURNING *")
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
        return Response(status=200, data=client_convert(res))

    def delete(self, request, pk):
        logger.info('DELETE Request for table Clients')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"DELETE FROM Clients WHERE id = {pk}")
        except AttributeError as exc:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=204, data='Content deleted')
