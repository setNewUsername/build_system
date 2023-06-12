from .base_purpose_handler import BasePurposeHandler

class RequestValidator:
    purposeHandlers:list[BasePurposeHandler] = None
    requesIpWhiteList:list = None
    purposeList:list = None

    def __init__(self, reqIpWhiteList, purposeHandlers:list[BasePurposeHandler] = None) -> None:
        self.purposeHandlers = purposeHandlers
        self.requesIpWhiteList = reqIpWhiteList
        self.purposeList = []
        self.createPurposesSlice()

    def createPurposesSlice(self):
        for handler in self.purposeHandlers:
            self.purposeList.append(handler.purposeName)

    def validateIp(self, ip) -> int:
        if not ip in self.requesIpWhiteList:
            return 104
        return 1

    def addPurposeHandlers(self, newPurposeHanlder) -> None:
        self.purposeHandlers.append(newPurposeHanlder)

    def validatePurpose(self, jsonData) -> tuple:
        if self.purposeHandlers == None or len(self.purposeHandlers) == 0:
            print ('Purpose handlers is None')
            return (105, '')
        
        if 'purpose' in jsonData.keys():
            curPurpose = jsonData['purpose']

            if curPurpose in self.purposeList:
                for handler in self.purposeHandlers:
                    if curPurpose == handler.purposeName:
                        return handler.validatePurposeFields(jsonData)
            else:
                return (102, '')
        else:
            return (101, '')