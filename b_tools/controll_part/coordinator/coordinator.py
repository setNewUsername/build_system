import sys, os, argparse, uuid, requests, json, threading
sys.path.append(f'{os.path.dirname(os.path.abspath(__file__))}\..\\')

from common.command_reciever import command_reciever as CR
from build_machine_model import BuildMachine
from queue import Queue
from purpose_handlers import *

#add call commands
parser = argparse.ArgumentParser()

parser.add_argument('--serverip', nargs='?', default='127.0.0.1')
parser.add_argument('--serverport', nargs='?', default='8000')

namespace = parser.parse_args(sys.argv[1:])
#add call commands

class Coordinator:
    coordinatorIp:str = None
    coordinatorPort:int = None

    buildMachines:dict[str, BuildMachine] = None
    projectQueue:Queue = None
    coordinatorAlive:bool = True
    projectsToRemoveFromQueue:list = None

    def __init__(self, coordIp, coordPort) -> None:
        self.coordinatorIp = coordIp
        self.coordinatorPort = int(coordPort)
        self.buildMachines = {}
        self.projectQueue = Queue()
        self.projectsToRemoveFromQueue = []

    def sendMessageToBuildMachine(self, machineId, message):
        machine = self.buildMachines[machineId]
        return requests.post(f'http://{machine.machineAdress}:{machine.machinePort}', data=json.dumps(message))

    def processBuildMachineResponse(self, response):
        print(response)

    def addBuildMachine(self, jsonData):
        #add machine validation
        newMachineId = uuid.uuid1()
        adress = jsonData['build_host_ip']
        port = jsonData['build_host_port']
        print(f'Added build machine')
        print(f'Machine id: {newMachineId}')
        print(f'Machine adress: {adress}; port: {port}')
        self.buildMachines[f'{newMachineId}'] = BuildMachine(adress, port)
        return (202, {
            'machine_id': f'{newMachineId}'
        })

    def removeBuildMachine(self, machineId):
        removedMachine = self.buildMachines.pop(machineId)
        print(f'Removed build machine')
        print(f'Machine id: {machineId}')
        print(f'Machine adress: {removedMachine.machineAdress}; port: {removedMachine.machinePort}')
        return (202, '')

    def markProjectForRemove(self, projectId):
        #add project validation
        if not projectId in self.projectsToRemoveFromQueue:
            print(f'Project marked as candidate to remove from queue; project id {projectId}')
            self.projectsToRemoveFromQueue.append(projectId)
            return (209, '')
        else:
            return (106, '')

    def addProjectToQueue(self, projectId):
        #add project validation
        if not projectId in self.projectsToRemoveFromQueue:
            print(f'Added new project to queue; project id: {projectId}')
            self.projectQueue.put(projectId)
            print(f'Project queue size: {self.projectQueue.qsize()}')
            return (202, {
                'queue_size': f'{self.projectQueue.qsize()}'
            })
        else:
            return (106, '')

    def stopProjectLoop(self):
        self.coordinatorAlive = False

    def startProjectsLoop(self):
        prjLoopThread = threading.Thread(target=self.projectsLoop, args=())
        prjLoopThread.start()

    def projectsLoop(self):
        while self.coordinatorAlive:
            if not self.projectQueue.empty():
                if len(self.buildMachines.keys()):
                    for buildMachineId in self.buildMachines.keys():
                        if self.buildMachines[buildMachineId].machineFree:
                            projectIdToStart = self.projectQueue.get()
                            if not projectIdToStart in self.projectsToRemoveFromQueue:
                                self.buildMachines[buildMachineId].machineFree = False
                                print(f'Project removed from queue; project id: {projectIdToStart}')
                                print(f'Project queue size: {self.projectQueue.qsize()}')
                                self.processBuildMachineResponse(self.sendMessageToBuildMachine(buildMachineId, {
                                    'purpose': 'start_build',
                                    'purpose_data':{
                                        'project_id': 'test_json'
                                    }
                                }))

coordinator = Coordinator(namespace.serverip, namespace.serverport)

#purpose handlers setup
startPHandler = StartBuildPurpose(['project_id'], coordinator.addProjectToQueue)
removePHandler = RemoveProjectFromQueuePurpose(['project_id'], coordinator.markProjectForRemove)
registerPHandler = RegisterMachinePurpose(['build_host_ip', 'build_host_port'], coordinator.addBuildMachine)
unRegisterPHandler = UnRegisterMachinePurpose(['machine_id'], coordinator.removeBuildMachine)
#purpose hanclders setup

reqVal = CR.RequestValidator(['192.168.0.107', '192.168.0.104'], purposeHandlers=[startPHandler, removePHandler, registerPHandler, unRegisterPHandler])

resHad = CR.ResponseHandler(reqVal)

def startServerFunc():
    print(f'Coordinator server started at {coordinator.coordinatorIp}:{coordinator.coordinatorPort}')
    coordinator.startProjectsLoop()

def closeServerFunc():
    coordinator.stopProjectLoop()
    print(f'Coordinator server stopped')

CR.CustomRequestHandler.responseHandler = resHad

httpd = CR.CustomHTTPServer(coordinator.coordinatorIp, coordinator.coordinatorPort, CR.CustomRequestHandler, sForeverF=startServerFunc, sCloseF=closeServerFunc)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()