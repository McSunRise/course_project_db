from django.http.response import HttpResponseServerError
from rest_framework.response import Response
from rest_framework.views import APIView
from course_project import settings
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
                res = cur.fetchall()
            db_commit(conn)
        except AttributeError:
            return HttpResponseServerError(content='Connection with database was NOT established')
        logger.info('Request successful')
        return Response(res)

# Create your views here.
