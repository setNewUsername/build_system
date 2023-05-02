from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import sys, argparse, requests, json, threading

sys.path.insert(0, '../../runner/')
sys.path.insert(0, '../../builder/')

from runner import *
from commons import *

print('start build_machine')

parser = argparse.ArgumentParser()

parser.add_argument('--coordinatorip', nargs='?', default='127.0.0.1')
parser.add_argument('--coordinatorport', nargs='?', default='8000')
parser.add_argument('--serverip', nargs='?', default='127.0.0.1')
parser.add_argument('--serverport', nargs='?', default='8001')

namespace = parser.parse_args(sys.argv[1:])

coordinatorData = {
    'purpose': 'register',
    'build_host_ip':namespace.serverip,
    'build_host_port':namespace.serverport
}

answer = requests.post(f'http://{namespace.coordinatorip}:{namespace.coordinatorport}', data=json.dumps(coordinatorData))

class Stopper:
    machineFree = True

class Builder(BaseHTTPRequestHandler):
    stopper:Stopper = Stopper()

    def _set_response(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._set_response(self.getData(post_data.decode('utf-8')))
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def startBuild(self, projectName):
        start(projectName)
        self.machineFree = True
        print('----build successefull----')

    def getData(self, data:str) -> int:
        options:dict = json.loads(data)
        print(options)
        if(options['purpose'] == 'start_build'):
            if self.stopper.machineFree:
                self.stopper.machineFree = False
                print('start build')
                thread = threading.Thread(target=self.startBuild, args=(options['project_name'],))
                thread.start()
                return 200
            else:
                return 503
        else:
            pass
        return 503

address = (namespace.serverip, int(namespace.serverport))

httpd = HTTPServer(address, Builder)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()