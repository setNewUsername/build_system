from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import sys, os, argparse, requests, json

print('start coordinator')

parser = argparse.ArgumentParser()

parser.add_argument('--serverip', nargs='?', default='127.0.0.1')
parser.add_argument('--serverport', nargs='?', default='8000')

namespace = parser.parse_args(sys.argv[1:])

class HTTPHandler(BaseHTTPRequestHandler):
    addHostFunction = None

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
        self.addHostFunction(options['build_host_ip'], options['build_host_port'])

class BuildHost:
    address = ''
    port = ''

    def __init__(self, address, port) -> None:
        self.address = address
        self.port = port

    def sendMessage(self, data):
        answer = requests.post(f'http://{self.address}:{self.port}', data=json.dumps(data))
        print(answer)

class Coordinator(BaseHTTPRequestHandler):
    buildHosts:list = []

    def addBuildHost(self, hostAddress, hostPort):
        noCollision:bool = True
        for i in range(self.buildHosts):
            if hostAddress == self.buildHosts[i].address:
                if hostPort != self.buildHosts[i][1]:
                    self.buildHosts[i].port = hostPort
                collision = False
                
        if noCollision:
            self.buildHosts.append(BuildHost(hostAddress, hostPort))
        print(f'build hosts amount: {len(self.buildHosts)}')

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
            data = {
                'purpose': 'start_build',
                'project_name': options['project_name']
            }
            for host in self.buildHosts:
                answer = requests.post(f'http://{host.address}:{host.port}', data=json.dumps(data))
                
        elif(options['purpose'] == 'build_finished'):
            pass
        else:
            pass

    def startUnMaintanedBuildServer(self, projectName):
        pass

address_tuple = (namespace.serverip, int(namespace.serverport))

httpd = HTTPServer(address_tuple, Coordinator)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()