import grpc
import generic_pb2
import generic_pb2_grpc

#Simple client to send a generic message to the server.

def run():
    # Crea un canal de comunicación gRPC hacia el servidor
    with grpc.insecure_channel('localhost:50051') as channel:
        # Crea un cliente gRPC
        stub = generic_pb2_grpc.DataServiceStub(channel)
        # Crea un mensaje Data para enviar al servidor
        data = generic_pb2.Data(
            data_type="geojson",
            payload=b"{'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [1.0, 2.0]}, 'properties': {}}"
        )
        # Envía el mensaje al servidor
        response = stub.SendData(data)
    print("Received response:", response)

if __name__ == '__main__':
    run()
