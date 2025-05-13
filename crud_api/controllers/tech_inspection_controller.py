from psycopg2.errors import ForeignKeyViolation

from .db_controller import *
from crud_api.serializers.tech_inspection_serializer import TechInsSerializer, tech_ins_convert

logger = logging.getLogger(__name__)


class TechInsList:
    def read(self, request):
        logger.info('GET Request for table Tech_Inspection')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute('SELECT * FROM Tech_Inspection')
                res = tech_ins_convert(cur.fetchall())
                serializer = TechInsSerializer(res, many=True)
        except AttributeError as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def create(self, request):
        logger.info('POST Request for table Tech_Inspection')
        conn = db_connect()
        data = TechInsSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"INSERT INTO Tech_Inspection (car_id, mechanic_id, work_type, work_cost) VALUES ("
                            f"{data.data['car_id']}, {data.data['mechanic_id']}, "
                            f"'{data.data['work_type']}', '{data.data['work_cost']}') "
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
        return Response(status=201, data=tech_ins_convert(res))


class TechInsDetails:
    def read(self, request, pk):
        logger.info(f'GET Request for table Tech_Inspection, row {pk}')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f'SELECT * FROM Tech_Inspection WHERE id = {pk}')
                res = tech_ins_convert(cur.fetchall())
                serializer = TechInsSerializer(res, many=True)
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=200, data=serializer.data)

    def update(self, request, pk):
        logger.info('PUT Request for table Tech_Inspection')
        conn = db_connect()
        data = TechInsSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"UPDATE Tech_Inspection SET car_id = {data.data['car_id']}, "
                            f"mechanic_id = {data.data['mechanic_id']}, work_type = '{data.data['work_type']}', "
                            f"work_cost = {data.data['work_cost']} WHERE id = {pk} RETURNING *")
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
        return Response(status=200, data=tech_ins_convert(res))

    def delete(self, request, pk):
        logger.info('DELETE Request for table Tech_Inspection')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f"DELETE FROM Tech_Inspection WHERE id = {pk}")
        except AttributeError as exc:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception as exc:
            logger.error(type(exc))
            logger.error(exc)
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=204, data='Content deleted')
