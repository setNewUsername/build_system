import sys, os
sys.path.append(f'{os.path.dirname(os.path.abspath(__file__))}\..\\')

from common.command_reciever import command_reciever as CR

class StartBuildPurpose(CR.BasePurposeHandler):
    def __init__(self, reqFields: list) -> None:
        super().__init__('start_build', reqFields, True)

    def purposeProcess(self, jsonData):
        print(jsonData)
        return 202

strH = StartBuildPurpose(['project_name'])

reqVal = CR.RequestValidator(['192.168.0.107'], purposeHandlers=[strH])

resHad = CR.ResponseHandler(reqVal)

def startServerFunc():
    print('Server started')

def closeServerFunc():
    print('Server stopped')

CR.CustomRequestHandler.responseHandler = resHad

httpd = CR.CustomHTTPServer('192.168.0.104', 8000, CR.CustomRequestHandler, sForeverF=startServerFunc, sCloseF=closeServerFunc)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()