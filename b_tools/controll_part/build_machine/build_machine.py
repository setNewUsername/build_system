import json, sys, os, argparse, requests, threading
sys.path.append('..\\..\\..\\')

from b_tools.controll_part.common.command_reciever import command_reciever as CR
from b_tools.build_part.builder.json_builder import *
from b_tools.build_part.runner.runner import start
from purpose_handlers import *

#add call commands

parser = argparse.ArgumentParser()

parser.add_argument('--coordinatorip', nargs='?', default='127.0.0.1')
parser.add_argument('--coordinatorport', nargs='?', default='8000')
parser.add_argument('--serverip', nargs='?', default='127.0.0.1')
parser.add_argument('--serverport', nargs='?', default='8001')

namespace = parser.parse_args(sys.argv[1:])

class BuildMachine:
    machineId:str = None
    machineAdress:str = None
    machinePort:int = None
    coordinatorAdress:str = None
    coordinatorPort:int = None
    machineIsFree:bool = True

    def __init__(self, machineAdr, machinePort, coordAdr, coordPort) -> None:
        self.machineAdress = machineAdr
        self.machinePort = int(machinePort)
        self.coordinatorAdress = coordAdr
        self.coordinatorPort = int(coordPort)

    def sendRequestToCoordinator(self, message):
        return requests.post(f'http://{self.coordinatorAdress}:{self.coordinatorPort}', data=json.dumps(message)).json()

    def stopBuild(self):
        pass

    def registerMachine(self):
        jsonData = self.sendRequestToCoordinator({
            'purpose': 'register_machine',
            'purpose_data':{
                'build_host_ip': bMachine.machineAdress,
                'build_host_port': bMachine.machinePort
            }
        })
        print(jsonData)
        self.machineId = jsonData['message_data']['machine_id']
        print(f'Got response from coordinator; machine id: {self.machineId}')

    def unregisterMachine(self):
        self.sendRequestToCoordinator({
            'purpose': 'unregister_machine',
            'purpose_data':{
                'machine_id': f'{self.machineId}',
            }
        })

    def startBuild(self, projectId):
        if self.machineIsFree:
            self.machineIsFree = False
            thread = threading.Thread(target=self.startBuildThread, args=(projectId,))
            thread.start()
            return (202, '')
        else:
            return (100, '')

    def startBuildThread(self, projectId):
        #start function is in runner.py file
        try:
            buildSuccess = start(projectId)
        except Exception as ex:
            print('Error while build: ', ex)
        print('Build finished')
        buildSuccess = True
        self.machineIsFree = True
        if buildSuccess:
            self.sendRequestToCoordinator({
                    'purpose': 'build_finished',
                    'purpose_data':{
                        'machine_id': f'{self.machineId}',
                    }
                })
        else:
            self.sendRequestToCoordinator({
                    'purpose': 'build_failed',
                    'purpose_data':{
                        'build_host_ip': self.machineAdress,
                        'build_host_port': self.machinePort
                    }
                })

bMachine = BuildMachine(namespace.serverip, namespace.serverport, namespace.coordinatorip, namespace.coordinatorport)

bMachine.registerMachine()

def startServerFunc():
    print(f'Build machine server started at {bMachine.machineAdress}:{bMachine.machinePort}')

def closeServerFunc():
    bMachine.unregisterMachine()
    print('Build machine server stopped')

startPHandler = StartBuildPurpose(['project_id'], bMachine.startBuild)

reqVal = CR.RequestValidator(['127.0.0.1'], purposeHandlers=[startPHandler])

resHad = CR.ResponseHandler(reqVal)

CR.CustomRequestHandler.responseHandler = resHad

httpd = CR.CustomHTTPServer(bMachine.machineAdress, bMachine.machinePort, CR.CustomRequestHandler, sForeverF=startServerFunc, sCloseF=closeServerFunc)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()