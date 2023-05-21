from request_validator import RequestValidator 
from err_succ_handlers import ErrorHandler, SuccessHandler, errHandler, succHandler


'''
100 - unhandled error
101 - no purpose field
102 - not supported purpose
103 - purpose wrong data
104 - host not in white list
105 - no purpose handlers
106 - project already marked as candidate to remove from build queue

201 - request completed
202 - build started
203 - build stopped
204 - build planned
205 - project files removed
206 - build machines amount checked
207 - machine registered
208 - machine unregistered
209 - project remove from queue
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

class ResponseWrapper:
    httpResponseCode = None
    jsonResponseData = None

    def __init__(self, code, data) -> None:
        self.httpResponseCode = code
        self.jsonResponseData = data

class ResponseHandler:
    requiestVal:RequestValidator = None
    errorHandler:ErrorHandler = None
    successHandler:SuccessHandler = None
    innerCodesToHttpCodes:dict = None

    def __init__(self, requestValidator:RequestValidator) -> None:
        self.requiestVal = requestValidator
        self.reqFiledFuncMap = {}

    def addInnerCodeToHttp(self, innerCode, httpCode) -> int:
        self.innerCodesToHttpCodes[innerCode] = httpCode

    def packMessageToWrapper(self, innerCode, messageData) -> ResponseWrapper:
        message = {}
        if not innerCode in self.innerCodesToHttpCodes.keys():
            return ResponseWrapper(200, {'message':'unhandled error'})
        if innerCode < 200:
            message['message'] = self.errorHandler.processError(innerCode)
            message['message_data'] = messageData
        elif innerCode < 300:
            message['message'] = self.successHandler.processSuccess(innerCode)
            message['message_data'] = messageData

        return ResponseWrapper(self.innerCodesToHttpCodes[innerCode], message)
    
    def processRequest(self, requesterIpAdress, jsonData) -> ResponseWrapper:
        valIpCode = self.requiestVal.validateIp(requesterIpAdress)
        if valIpCode == 1:
            data = self.requiestVal.validatePurpose(jsonData)
            return self.packMessageToWrapper(data[0], data[1])
        else:
            return self.packMessageToWrapper(valIpCode, '')

ResponseHandler.errorHandler = errHandler
ResponseHandler.successHandler = succHandler

ResponseHandler.innerCodesToHttpCodes = {
    #err messages codes
    201: 200,
    202: 200,
    203: 200,
    204: 200,
    205: 200,
    206: 200,
    207: 200,
    208: 200,
    209: 200,
    #succ messages codes
    100: 200,
    101: 200,
    102: 200,
    103: 200,
    104: 200,
    105: 200,
    106: 200
}