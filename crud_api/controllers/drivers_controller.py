from .db_controller import *
from ..serializers.drivers_serializer import DriversSerializer, driver_convert

logger = logging.getLogger(__name__)


class DriversList:
    def read(self, request):
        logger.info('GET Request for table Drivers')
        conn = db_connect()
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute('SELECT * FROM Drivers')
                res = driver_convert(cur.fetchall())
                serializer = DriversSerializer(res, many=True)
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        logger.info('Request successful')
        db_commit(conn)
        return Response(serializer.data)

    def create(self, request):
        logger.info('POST Request for table Drivers')
        conn = db_connect()
        data = DriversSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            with conn.cursor() as cur:
                cur.execute('SET search_path TO course_project')
                cur.execute(f'INSERT INTO Drivers (name, license_number, phone) VALUES '
                            f"('{data.data['name']}', '{data.data['license_number']}', '{data.data['phone']}')"
                            f"RETURNING *")
                res = cur.fetchall()
        except AttributeError:
            return Response(status=500, data='Connection with database was NOT established')
        except Exception:
            return Response(status=500, data='Something went wrong')
        logger.info('Request successful')
        db_commit(conn)
        return Response(status=201, data=driver_convert(res))
