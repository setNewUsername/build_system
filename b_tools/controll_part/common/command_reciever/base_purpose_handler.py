import threading

class BasePurposeHandler:
    purposeName:str = ''
    purposeRequiredFields:list = None
    blocking:bool = None

    def __init__(self, name:str, reqFields:list, isBlocking:bool) -> None:
        self.purposeName = name
        self.purposeRequiredFields = reqFields
        self.blocking = isBlocking

    def validatePurposeFields(self, jsonData):
        curFields = jsonData['purpose_data']

        for reqField in self.purposeRequiredFields:
            if not reqField in curFields:
                return (103, '')
        if not self.blocking:
            newPurposeProcessThread = threading.Thread(target=self.purposeProcess, args=(jsonData,))
            newPurposeProcessThread.start()
        else:
            return self.purposeProcess(jsonData)
        return 1

    def purposeProcess(self, jsonData) -> tuple:
        print('No purposeProcess realisation')