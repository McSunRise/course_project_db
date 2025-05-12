from .db_controller import *
from ..serializers.cars_serializer import CarsSerializer, car_convert

logger = logging.getLogger(__name__)


class CarsList:
    def read(self, request):
        logger.info('GET Request for table Cars')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute('SELECT * FROM Cars')
                res = car_convert(cur.fetchall())
                serializer = CarsSerializer(res, many=True)
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(serializer.data)

    def create(self, request):
        logger.info('POST Request for table Cars')
        conn = db_connect()
        data = CarsSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f'INSERT INTO Cars (model, license_plate, driver_id) VALUES '
                            f"('{data.data['model']}', '{data.data['license_plate']}', {data.data['driver_id']})"
                            f"RETURNING *")
                res = cur.fetchall()
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception:
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=201, data=car_convert(res))
