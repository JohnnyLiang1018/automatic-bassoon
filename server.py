from http import server
import socket
from ast import literal_eval
from vectorizedGym import VectorizedGym
import torch as torch
import numpy as np
import pickle
import requests
import base64
import torch


class Server(object):

    def __init__(self):
        self.gym = VectorizedGym()
        self.num_ensemble = 2

    def server_program(self):
        host = socket.gethostname()
        port = 4777 

        server_socket = socket.socket()
        server_socket.bind((host, port))

        server_socket.listen(1)
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        data_string = pickle.dumps(self.gym.obs_i)
        conn.send(data_string)
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024)
            actions = pickle.loads(data)
            if actions != None:
                print("from connected user: " + str(actions))
                obs, reward, done, info =  self.gym.take_actions(actions)
                data = pickle.dumps((obs,reward,done,info))
                conn.send(data)
    
    def test(self,policy):
        base64_byte = base64.b64encode(policy)
        base64_string = base64_byte.decode("ascii")
        json = {"numEnsemble": 3, "policy": [base64_string]}
        response = requests.post("http://localhost:8081/request", json=json)
        return response.text
        
        base64.dec
    
server = Server()
server.server_program()

# if __name__ == '__main__':
#     server_program()
# model = torch.nn.Linear(4,2)
# x = torch.randn(4)
# torch.onnx.export(model, x,'test.onnx',export_params=True)
# with open('test.onnx','rb') as handle:
#     print(server.test(handle))