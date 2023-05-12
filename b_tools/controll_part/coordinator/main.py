from collections.abc import Callable
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import sys, os, argparse, requests, json, threading
from typing import Any
from queue import Queue

parser = argparse.ArgumentParser()

parser.add_argument('--serverip', nargs='?', default='127.0.0.1')
parser.add_argument('--serverport', nargs='?', default='8000')

namespace = parser.parse_args(sys.argv[1:])

class BuildHost:
    address = ''
    port = ''
    maintained:bool = False

    def __init__(self, address, port) -> None:
        self.address = address
        self.port = port

    def sendMessage(self, data):
        return requests.post(f'http://{self.address}:{self.port}', data=json.dumps(data))

class Stopper:
    cont = True

    def __init__(self, state) -> None:
        self.cont = state

class Coordinator(BaseHTTPRequestHandler):
    buildHosts:list = []
    projectsQueue:Queue = Queue()
    coordinatorIsAlive:Stopper

    def __init__(self, request, client_address, server) -> None:
        thread = threading.Thread(target=self.doLoop, args=(self.coordinatorIsAlive,))
        thread.start()
        super().__init__(request, client_address, server)

    def doLoop(self, aliveCondition:Stopper):
        while aliveCondition.cont:
            if not self.projectsQueue.empty():
                if len(self.buildHosts) > 0:
                    for host in self.buildHosts:
                        if not host.maintained:
                            host.maintained = True
                            host.sendMessage({
                                'purpose': 'start_build',
                                'project_name': self.projectsQueue.get()
                            })
                            break

    def changeBuildHostMaintainToFalse(self, hostIp:str, hostPort:str):
        for host in self.buildHosts:
            if hostIp == host.address and hostPort == host.port:
                host.maintained = False
                return

    def addBuildHost(self, hostAddress, hostPort):
        noCollision:bool = True
        #uncomment
        '''
        for i in range(len(self.buildHosts)):
            if hostAddress == self.buildHosts[i].address:
                if hostPort != self.buildHosts[i].port:
                    self.buildHosts[i].port = hostPort
                noCollision = False
        '''
        if noCollision:
            newHost = BuildHost(hostAddress, hostPort)
            self.buildHosts.append(newHost)
        print(f'build hosts amount: {len(self.buildHosts)}')
        for host in self.buildHosts:
            print(f'host ip: {host.address}; host port: {host.port}')

    def removeBuildHost(self, hostAddress, hostPort):
        self.buildHosts.remove(BuildHost(hostAddress, hostPort))
        print(f'build hosts amount: {len(self.buildHosts)}')

    def setAddFunc(self, addHostFunc):
        self.addHostFunction = addHostFunc

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.getData(post_data.decode('utf-8'))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def getData(self, data:str):
        options:dict = json.loads(data)
        print(options)
        if(options['purpose'] == 'register'):
            self.addBuildHost(options['build_host_ip'], options['build_host_port'])
        elif(options['purpose'] == 'unregister'):
            self.removeBuildHost(options['build_host_ip'], options['build_host_port'])
        elif(options['purpose'] == 'start_build'):
            self.projectsQueue.put(options['project_name'])
            print(f'Added new project to build queue; name = { options["project_name"] }')
            print(f'Projects in queue: {self.projectsQueue.qsize()}')
        elif(options['purpose'] == 'build_finished'):
            self.changeBuildHostMaintainToFalse(options['build_host_ip'], options['build_host_port'])
        else:
            pass

class CustomHTTPServer(HTTPServer):

    stopCoord:Stopper = Stopper(True)

    def __init__(self, server_address, RequestHandlerClass:Coordinator, bind_and_activate:bool = True) -> None:
        RequestHandlerClass.coordinatorIsAlive = self.stopCoord
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

    def serve_forever(self, poll_interval: float = 0.5) -> None:
        print('Server started')
        return super().serve_forever(poll_interval)

    def server_close(self) -> None:
        print('Server closed')
        self.stopCoord.cont = False
        return super().server_close()

address_tuple = (namespace.serverip, int(namespace.serverport))

httpd = CustomHTTPServer(address_tuple, Coordinator)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()