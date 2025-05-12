from .db_controller import *
from ..serializers.clients_serializer import ClientsSerializer, client_convert

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
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(serializer.data)

    def create(self, request):
        logger.info('POST Request for table Clients')
        conn = db_connect()
        data = ClientsSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f'INSERT INTO Clients (name, email, phone) VALUES '
                            f"('{data.data['name']}', '{data.data['email']}', '{data.data['phone']}')"
                            f"RETURNING *")
                res = cur.fetchall()
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception:
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=201, data=client_convert(res))
