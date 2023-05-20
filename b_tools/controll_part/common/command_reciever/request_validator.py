class RequestValidator:
    purposeHandlers:list = None
    requesIpWhiteList:list = None

    def __init__(self, reqIpWhiteList, purposeHandlers:list = None) -> None:
        self.purposeHandlers = purposeHandlers
        self.requesIpWhiteList = reqIpWhiteList

    def validateIp(self, ip) -> int:
        if not ip in self.requesIpWhiteList:
            return 104
        return 1

    def addPurposeHandlers(self, newPurposeHanlder) -> None:
        self.purposeHandlers.append(newPurposeHanlder)

    def validatePurpose(self, jsonData) -> int:
        if self.purposeHandlers == None or len(self.purposeHandlers) == 0:
            print ('Purpose handlers if None')
            return 105
        
        if 'purpose' in jsonData.keys():
            curPurpose = jsonData['purpose']

            for handler in self.purposeHandlers:
                if curPurpose == handler.purposeName:
                    return handler.validatePurposeFields(jsonData)
                return 102
        else:
            return 101