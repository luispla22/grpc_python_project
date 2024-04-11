import cv2
import datetime as dt
import argparse
import numpy as np
import grpc
import random
import frame_pb2
import frame_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp

'''
This script captures frames from a webcam, processes them, and sends them to a gRPC server. 
It provides options to save images, draw circles on frames, and set the capture interval. 
The captured frames are encoded as JPEG images and sent to the server along with a timestamp using Google Protocol Buffers (protobuf). 
Additionally, it allows customization of camera index, saving images, drawing circles on frames, and setting the capture interval through command-line arguments.
'''

path = './frames/'

#A function to make any process to frames (this draw a circle on it)
def draw_circle(frame):
    height, width, _ = frame.shape
    center = (width // 2, height // 2)
    radius = min(width, height) // 4
    cv2.circle(frame, center, radius, (0, 255, 0), 2)


def send_frame_stub(stub, frame):
    # Serialize frame data into bytes
    _, frame_encoded = cv2.imencode('.jpg', frame)
    frame_bytes=bytes(frame_encoded)

    # Crear un objeto Timestamp de Google Protobuf

    timestamp=Timestamp()
    timestamp.GetCurrentTime()
    timestamp=timestamp
    # Crear el mensaje Frame con los datos del frame y el timestamp
    frame_message = frame_pb2.Frame(data=frame_bytes, timestamp=timestamp)
    
    # Enviar el mensaje al servidor
    response = stub.SendFrame(frame_message)

    # Manejar la respuesta (si es necesario)
    print("Frame sent successfully.")



def main(camera_index=0, save_images=False, draw_circle_enabled=False, capture_interval=30):
    capture = cv2.VideoCapture(camera_index)
    tiempoA = dt.datetime.now()
    tiempoTranscurrido = dt.timedelta()

    while capture.isOpened():
        ret, frame = capture.read()
        if ret:
            tiempoB = dt.datetime.now()
            tiempoTranscurrido += tiempoB - tiempoA

            if draw_circle_enabled:
                draw_circle(frame)

            cv2.imshow("webCam", frame)

            if tiempoTranscurrido.seconds >= capture_interval:

                with grpc.insecure_channel('localhost:50051') as channel:
                    stub = frame_pb2_grpc.FrameSenderStub(channel)
                    send_frame_stub(stub, frame)

                
                tiempoTranscurrido = dt.timedelta()
                tiempoA = dt.datetime.now()

                if save_images:
                    filename = dt.datetime.now().strftime('IMG-%Y-%m-%d-%H%M%S') + '.jpg'
                    cv2.imwrite(path+filename, frame)
                    print(f"Guardada captura: {filename}")
            
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            break
    
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--save", help="Guardar capturas", action="store_true")
    parser.add_argument("--circle", help="Dibujar círculo en las capturas", action="store_true")
    parser.add_argument("-i", "--interval", dest="capture_interval", help="Intervalo de tiempo en segundos para captura", type=int, default=3)
    parser.add_argument("-c", "--camera", dest="camera_index", help="Índice de la cámara a utilizar", type=int, default=0)
    args = parser.parse_args()

    main(camera_index=args.camera_index, save_images=args.save, draw_circle_enabled=args.circle, capture_interval=args.capture_interval)
