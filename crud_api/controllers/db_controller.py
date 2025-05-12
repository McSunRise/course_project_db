import logging
import psycopg2
from course_project import settings
from rest_framework.response import Response

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
        return Response(status=500, data='Connection with database was NOT established')
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