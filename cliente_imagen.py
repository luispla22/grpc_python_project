import grpc
import generic_pb2
import generic_pb2_grpc

#Simple client to send a image to the server and receive a response.

def run():
    # Crea un canal de comunicación gRPC hacia el servidor
    with grpc.insecure_channel('localhost:50051') as channel:
        # Crea un cliente gRPC
        stub = generic_pb2_grpc.DataServiceStub(channel)
        # Lee el contenido de la imagen desde un archivo
        with open('baloncesto.jpg', 'rb') as f:
            image_content = f.read()
        # Crea un mensaje Data para enviar al servidor, especificando el tipo como "imagen"
        data = generic_pb2.Data(
            data_type="imagen",
            payload=image_content
        )
        # Envía el mensaje al servidor
        response = stub.SendData(data)
    print("Received response:", response)

if __name__ == '__main__':
    run()
