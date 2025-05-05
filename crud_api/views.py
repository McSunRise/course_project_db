from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from course_project import settings
import logging
import psycopg2

logger = logging.getLogger(__name__)


def db_connect() -> object:
    logger.info('Establishing connection with database')
    db_settings = settings.DATABASES['default']
    conn = psycopg2.connect(
        dbname=db_settings['NAME'],
        user=db_settings['USER'],
        password=db_settings['PASSWORD'],
        host=db_settings['HOST'],
        port=db_settings['PORT'])
    cur = conn.cursor()
    cur.execute('SET search_path TO course_project')
    logger.info('Connection established successfully')
    return cur, conn


def db_commit(cur: object, conn: object):
    conn.commit()
    cur.close()
    conn.close()


class Home(APIView):
    def get(self, request: object) -> object:
        logger.info('GET Request for table Orders')
        cur, conn = db_connect()
        cur.execute('SELECT * FROM Orders')
        res = cur.fetchall()
        db_commit(cur, conn)
        logger.info('Request successful')
        return HttpResponse(res)

# Create your views here.
