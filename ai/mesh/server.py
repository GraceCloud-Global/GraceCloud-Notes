import grpc
from concurrent import futures
import control_pb2, control_pb2_grpc
import time

class ControlServicer(control_pb2_grpc.ControlMeshServicer):
    def SendCommand(self, request, context):
        print(f'📡 Received command: {request.action} → {request.service}')
        return control_pb2.CommandResponse(status='ok', message=f'{request.service} {request.action} executed')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    control_pb2_grpc.add_ControlMeshServicer_to_server(ControlServicer(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    print('🕹️ Control Mesh listening on 50055')
    while True:
        time.sleep(86400)

if __name__ == "__main__":
    serve()
