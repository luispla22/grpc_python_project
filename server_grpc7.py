import grpc
from concurrent import futures
import generic_pb2_grpc, gps_1403_pb2, gps_1403_pb2_grpc
import frame_pb2
import frame_pb2_grpc
import cv2
import time
# import gpsdata_pb2
# import gpsdata_pb2_grpc


from PIL import Image
import io
import os
import datetime
import requests

'''
This script implements a gRPC server that can receive various types of data, including images, GPS data, and generic payloads. 
It saves received data to files and optionally sends images to a Telegram bot.
It includes gRPC service implementations for handling different data types, such as DataService for generic data, 
DataGPSService for GPS data, and FrameSenderServicer for image frames. The script also contains utility functions 
for sending text and image messages to a Telegram bot.
'''


class DataService(generic_pb2_grpc.DataServiceServicer):
    def SendData(self, request, context):
        data_type = request.data_type
        payload = request.payload

        if data_type == "imagen":
            try:
                # Convierte los datos de la imagen en un objeto de imagen utilizando Pillow
                image = Image.open(io.BytesIO(payload))
                # Define el nombre del archivo de imagen que deseas utilizar
                nombre_archivo = f"imagen_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                # Guarda la imagen con el nombre de archivo especificado
                image.save("./received_frames/"+nombre_archivo)
                print(f"Imagen guardada como {nombre_archivo}")
            except Exception as e:
                print("Error al procesar la imagen:", e)
        else:
            # Si no es una imagen, almacena el texto en un archivo de texto
            try:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open('datos_recibidos.txt', 'a') as f:
                    f.write(f"Tipo de datos: {data_type}\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Payload: {payload}\n\n")
                print("Datos almacenados en el archivo 'datos_recibidos.txt'.")
                if data_type=="geojson":
                    print("Detectado")
            except Exception as e:
                print("Error al almacenar los datos:", e)

        
        return request

        
class DataGPSService(gps_1403_pb2_grpc.DataGPSServiceServicer):
    def SendGPSData(self, request, context):
        # Manejar el mensaje recibido
        print("Datos GPS recibidos:")
        print("Payload:", request.payload)
        print("Timestamp:", request.timestamp)
        if "FeatureCollection" in request.payload:
            telegram_bot_sendtext(request.payload)
        return gps_1403_pb2.DataGPS(payload="Datos recibidos correctamente", timestamp=request.timestamp)
    

class FrameSenderServicer(frame_pb2_grpc.FrameSenderServicer):
    def SendFrame(self, request, context):
        # Guardar los datos del frame en un archivo de imagen
        archivo_path = os.path.join('received_frames', f'frame_{request.timestamp.seconds}_{request.timestamp.nanos}.jpg')
        with open(archivo_path, 'wb') as f:
            f.write(request.data)
        #Telegram
        if datetime.datetime.now().weekday() == 4: #Simple condition to choose when to send the image (now it sends it if it is friday)
            telegram_bot_sendimage(archivo_path)
        
        # Imprimir la marca de tiempo del frame recibido
        print("Received frame with timestamp:", request.timestamp)
        time.sleep(1)
        # Devolver un mensaje Empty para indicar que se ha recibido el frame correctamente
        return frame_pb2.Void()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    generic_pb2_grpc.add_DataServiceServicer_to_server(DataService(), server)
    gps_1403_pb2_grpc.add_DataGPSServiceServicer_to_server(DataGPSService(), server)
    frame_pb2_grpc.add_FrameSenderServicer_to_server(FrameSenderServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Starting server. Listening on port 50051...")
    server.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop(0)
        
bot_token = os.getenv('BOT_TOKEN')
bot_chatID = os.getenv('BOT_CHAT_ID')
        
def telegram_bot_sendtext(bot_message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def telegram_bot_sendimage(image_path):
    send_image = 'https://api.telegram.org/bot' + bot_token + '/sendPhoto'
    files = {'photo': open(image_path, 'rb')}
    data = {'chat_id': bot_chatID}

    response = requests.post(send_image, files=files, data=data)
    
    return response.json()

if __name__ == '__main__':
    serve()
    