import json, sys, os, argparse, requests, threading, time
sys.path.append('..\\..\\..\\')

from b_tools.controll_part.common.command_reciever import command_reciever as CR
from b_tools.build_part.builder.json_builder import *
from b_tools.build_part.runner.runner import start
from purpose_handlers import *

#add call commands

parser = argparse.ArgumentParser()

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

    server:CR.CustomHTTPServer = None

    def __init__(self, machineAdr, machinePort) -> None:
        self.machineAdress = machineAdr
        self.machinePort = int(machinePort)

    def setCoordinatorInfo(self, data):
        self.coordinatorAdress = data['purpose_data']['coordinator_ip']
        self.coordinatorPort = int(data['purpose_data']['coordinator_port'])
        print(self.coordinatorAdress)
        print(self.coordinatorPort)
        return (201, 'new coordinator info setted')

    def sendRequestToCoordinator(self, message):
        return requests.post(f'http://{self.coordinatorAdress}:{self.coordinatorPort}', data=json.dumps(message)).json()

    def stopBuild(self):
        pass

    def registerMachine(self, data):
        if self.coordinatorAdress == None or self.coordinatorPort == None:
            return (100, 'no coordinator data supplied')
        try:
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
        except:
            return (100, 'error while registering occured')
        return (201, 'machine registrated successefully')

    def unregisterMachine(self, data):
        if self.machineId != None:
            tmp = self.machineId
            self.machineId = None
            try:
                self.sendRequestToCoordinator({
                    'purpose': 'unregister_machine',
                    'purpose_data':{
                        'machine_id': f'{tmp}',
                    }
                })
            except:
                return (100, 'error while unregistering occured')
            return (201, 'machine unregistered successefully')
        else:
            return (100, 'no machine id supplied; may be it wasn\'t registered')

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

bMachine = BuildMachine(namespace.serverip, namespace.serverport)

#bMachine.setCoordinatorInfo(namespace.coordinatorip, namespace.coordinatorport)

#bMachine.registerMachine()

def startServerFunc():
    print(f'Build machine server started at {bMachine.machineAdress}:{bMachine.machinePort}')

def closeServerFunc():
    bMachine.unregisterMachine(None)
    print('Build machine server stopped')

startPHandler = StartBuildPurpose(['project_id'], bMachine.startBuild)
setCoordinatorInfo = setCoordInfoPurpose(['coordinator_ip', 'coordinator_port'], bMachine.setCoordinatorInfo)
registerMachine = regMachinePurposer(['placeholder'], bMachine.registerMachine)
unregMachine = unregMachinePurpose(['placeholder'], bMachine.unregisterMachine)

reqVal = CR.RequestValidator(None, purposeHandlers=[startPHandler, setCoordinatorInfo, registerMachine, unregMachine])

resHad = CR.ResponseHandler(reqVal)

CR.CustomRequestHandler.responseHandler = resHad

httpd = CR.CustomHTTPServer(bMachine.machineAdress, bMachine.machinePort, CR.CustomRequestHandler, sForeverF=startServerFunc, sCloseF=closeServerFunc)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()