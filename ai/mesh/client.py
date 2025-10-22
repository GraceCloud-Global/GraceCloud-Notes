import grpc, control_pb2, control_pb2_grpc

def send(service, action):
    channel = grpc.insecure_channel('localhost:50055')
    stub = control_pb2_grpc.ControlMeshStub(channel)
    resp = stub.SendCommand(control_pb2.CommandRequest(service=service, action=action))
    print(f'✅ Response: {resp.status} — {resp.message}')

if __name__ == "__main__":
    send('api', 'reload')
