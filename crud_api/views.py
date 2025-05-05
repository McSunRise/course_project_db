from django.http.response import HttpResponseServerError
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from course_project import settings
from .serializers import OrdersSerializer, order_convert, OrdersDM
import logging
import psycopg2

logger = logging.getLogger(__name__)


def db_connect() -> object:
    logger.info('Establishing connection with database')
    db_settings = settings.DATABASES['default']
    try:
        conn = psycopg2.connect(
            dbname=db_settings['NAME'],
            user=db_settings['USER'],
            password=db_settings['PASSWORD'],
            host=db_settings['HOST'],
            port=db_settings['PORT'])
    except UnicodeDecodeError:
        logger.error('Connection with database was NOT established')
        return HttpResponseServerError(content='Connection with database was NOT established')
    logger.info('Connection established successfully')
    return conn


def db_commit(conn: object):
    conn.commit()
    logger.info('Changes commited')
    conn.close()
    logger.info('Connection closed')


def db_rollback(conn: object):
    conn.rollback()
    logger.info('Changes rolled back')
    conn.close()
    logger.info('Connection closed')


class Orders(APIView):
    def get(self, request: object) -> object:
        logger.info('GET Request for table Orders')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute('SELECT * FROM Orders')
                res = order_convert(cur.fetchall())
                serializer = OrdersSerializer(res, many=True)
        except AttributeError:
            return HttpResponseServerError(content='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(serializer.data)

    def post(self, request):
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
        except Exception:
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=201, data=order_convert(res))

# Create your views here.
