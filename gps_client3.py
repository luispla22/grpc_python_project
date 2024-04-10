import requests
import serial
import grpc
import geojson
import gps_1403_pb2
import gps_1403_pb2_grpc

from google.protobuf.timestamp_pb2 import Timestamp


# This script establishes a connection with a GPS device via serial communication, reads GPS data, parses it, 
# generates GeoJSON data, and sends it to a gRPC server. It includes functions to analyze serial ports, connect to GPS, 
# parse GPS data, generate GeoJSON, connect to the gRPC server, and a main function to orchestrate these tasks.



'''
def obtener_direccion(lat, lon):
    response = requests.get(f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}')
    address = response.json().get('address')
    return address
'''
def generar_geojson(latitud, longitud):
    if latitud is not None and longitud is not None:
        # Crear un objeto Point
        punto = geojson.Point((longitud, latitud))

        # Crear un objeto Feature usando el punto
        feature = geojson.Feature(geometry=punto)

        # Crear una colección de características (solo tenemos una en este caso)
        feature_collection = geojson.FeatureCollection([feature])

        # Convertir la colección de características a GeoJSON
        geojson_str = geojson.dumps(feature_collection, indent=2)
        if geojson_str is not None:
            conectar_server(geojson_str)


        return geojson_str
    else:
        return None
    
def parsear_linea_gps(line):
    # Decodifica la línea de bytes a una cadena de texto
    line = line.decode('utf-8')
    # Divide la línea en partes
    parts = line.split(',')
    if parts[0] == '$GPGGA':
        # Obtiene la latitud y la longitud de la línea GPGGA
        lat = float(parts[2][:2]) + float(parts[2][2:]) / 60 if parts[2] else None
        if parts[3] == 'S':
            lat = -lat
        lon = float(parts[4][:3]) + float(parts[4][3:]) / 60 if parts[4] else None
        if parts[5] == 'W':
            lon = -lon
        geojson_data = generar_geojson(lat, lon)
        return lat, lon, geojson_data
    else:
        return None, None, None




def buscar_puerto_en_uso():
    print("Analizando puertos serie...")
    for i in range(1, 16):
        try:
            puerto = serial.Serial(f'COM{i}')
            puerto.close()
            print(f'El puerto COM{i} está en uso.')
            return f'COM{i}'
        except serial.SerialException:
            print(f'El puerto COM{i} está libre.')
    return None

def conectar_gps(puerto):
    print("Estableciendo conexión con GPS...")
    if puerto is not None:
        gps = serial.Serial(puerto, baudrate=4800, timeout=1)
        while True:
            line = gps.readline()
            print(line)
            lat, lon,geojsondata = parsear_linea_gps(line)
            #if lat and lon:
                #address = obtener_direccion(lat, lon)
                #print(f'La dirección encontrada es: {address}')
            print(lat,lon)
            print("geojson: ",geojsondata)
    else:
        print("No se encontró ningún puerto en uso.")
        
def conectar_server(string):
      # Crea un canal de comunicación gRPC hacia el servidor
    with grpc.insecure_channel('localhost:50051') as channel:
        # Crea un cliente gRPC
        stub = gps_1403_pb2_grpc.DataGPSServiceStub(channel)
        # Crea un mensaje Data para enviar al servidor
        timestamp=Timestamp()
        timestamp.GetCurrentTime()
        data = gps_1403_pb2.DataGPS(
            payload=string,
            timestamp=timestamp
        )
        # Envía el mensaje al servidor
        response = stub.SendGPSData(data)
    print("Received response:", response)
    
    
    
def main():
    puerto_en_uso = buscar_puerto_en_uso()
    conectar_gps(puerto_en_uso)

if __name__ == "__main__":
    main()

'''
NMEA:
    $GPGGA: Esta es una sentencia que proporciona información sobre el Fix GPS, que incluye la hora, la latitud, la longitud y
    otros datos relacionados con el fix. 

    $GPGSA: Esta sentencia proporciona información sobre el DOP (Dilution of Precision) y los satélites activos. 

    $GPRMC: Esta es una sentencia que proporciona información mínima recomendada específica del GPS. 

    $GPGSV: Esta sentencia proporciona información sobre los satélites en vista. En tu caso, parece que no hay satélites en vista, ya que todos los campos relevantes están vacíos.
'''