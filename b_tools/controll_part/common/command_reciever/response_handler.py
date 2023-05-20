from request_validator import RequestValidator 
from err_succ_handlers import ErrorHandler, SuccessHandler, errHandler, succHandler

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

    def packMessageToWrapper(self, innerCode) -> ResponseWrapper:
        message = {}
        if innerCode < 200:
            message['message'] = self.errorHandler.processError(innerCode)
        elif innerCode < 300:
            message['message'] = self.successHandler.processSuccess(innerCode)

        return ResponseWrapper(self.innerCodesToHttpCodes[innerCode], message)
    
    def processRequest(self, requesterIpAdress, jsonData) -> ResponseWrapper:
        valIpCode = self.requiestVal.validateIp(requesterIpAdress)
        if valIpCode == 1:
            return self.packMessageToWrapper(self.requiestVal.validatePurpose(jsonData))
        else:
            return self.packMessageToWrapper(valIpCode)

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
    #succ messages codes
    101: 200,
    102: 200,
    103: 200,
    104: 200,
    105: 200
}

