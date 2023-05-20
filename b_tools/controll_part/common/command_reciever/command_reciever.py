import json, sys, os
sys.path.append(f'{os.path.dirname(os.path.abspath(__file__))}\\')

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from response_handler import *
from base_purpose_handler import BasePurposeHandler

'''
101 - no purpose field
102 - not supported purpose
103 - purpose wrong data
104 - host not in white list
105 - no purpose handlers

201 - request completed
202 - build started
203 - build stopped
204 - build planned
205 - project files removed
206 - build machines amount checked
207 - machine registered
208 - machine unregistered
'''

'''
outer purposes:
start_build
stop_build
plan_build
remove_project_files
remove_user_projects
check_build_machines_amount

inner purposes:
register_machine
unregister_machine
'''

class CustomRequestHandler(BaseHTTPRequestHandler):
    responseHandler:ResponseHandler = None

    def __init__(self, request, client_address, server) -> None:
        super().__init__(request, client_address, server)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        responseData = self.processData(self.client_address[0], post_data.decode('utf-8'))
        self.send_response(responseData.httpResponseCode)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(json.dumps(responseData.jsonResponseData).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('<html><head><meta charset="utf-8">'.encode())
        self.wfile.write('<title>Простой HTTP-сервер.</title></head>'.encode())
        self.wfile.write('<body>Был получен GET-запрос.</body></html>'.encode())

    def processData(self, clientIp, data:str) -> ResponseWrapper:
        options:dict = json.loads(data)
        return self.responseHandler.processRequest(clientIp, options)
        
class CustomHTTPServer(HTTPServer):
    serverForeverFunc = None
    serverCloseFunc = None

    def __init__(self, serverIp, serverPort, RequestHandlerClass, bind_and_activate:bool = True, sForeverF = None, sCloseF = None) -> None:
        super().__init__((serverIp, serverPort), RequestHandlerClass, bind_and_activate)
        if sForeverF == None:
            self.serverForeverFunc = self.notDefinedFunction
        else:
            self.serverForeverFunc = sForeverF
        if sCloseF == None:
            self.serverCloseFunc = self.notDefinedFunction
        else:
            self.serverCloseFunc = sCloseF

    def notDefinedFunction(self):
        print(f'Function not defined')

    def serve_forever(self, poll_interval: float = 0.5) -> None:
        self.serverForeverFunc()
        return super().serve_forever(poll_interval)

    def server_close(self) -> None:
        self.serverCloseFunc()
        return super().server_close()

if __file__ == 'commad_reciever':

    class StartBuildPurpose(BasePurposeHandler):
        def __init__(self, reqFields: list) -> None:
            super().__init__('start_build', reqFields, True)

        def purposeProcess(self, jsonData):
            print(jsonData)
            return 202

    strH = StartBuildPurpose(['project_name'])

    reqVal = RequestValidator(['192.168.0.107'], purposeHandlers=[strH])

    resHad = ResponseHandler(reqVal)

    def startServerFunc():
        print('Server started')

    def closeServerFunc():
        print('Server stopped')

    CustomRequestHandler.responseHandler = resHad

    httpd = CustomHTTPServer('192.168.0.104', 8000, CustomRequestHandler, sForeverF=startServerFunc, sCloseF=closeServerFunc)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()